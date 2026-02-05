use reqwest::Client;
use serde::Deserialize;
use std::collections::HashMap;
use url::form_urlencoded;

#[derive(Deserialize)]
struct RabbitQueue {
    name: String,
    messages: u64,
}

#[derive(Deserialize)]
struct RabbitResponse {
    items: Vec<RabbitQueue>,
}

pub async fn get_queue_lengths(
    host: &str,
    port: &str,
    user: &str,
    pass: &str,
    pattern: &str,
) -> Result<HashMap<String, u64>, Box<dyn std::error::Error>> {
    let client = Client::new();
    let safe_pattern: String = form_urlencoded::byte_serialize(pattern.as_bytes()).collect();
    
    let url = format!(
        "http://{}:{}/api/queues?page=1&page_size=500&name={}&use_regex=true&pagination=true",
        host, port, safe_pattern
    );

    let res = client
        .get(&url)
        .basic_auth(user, Some(pass))
        .send()
        .await?
        .json::<RabbitResponse>()
        .await?;

    let mut ret = HashMap::new();
    for queue in res.items {
        ret.insert(queue.name, queue.messages);
    }

    Ok(ret)
}
