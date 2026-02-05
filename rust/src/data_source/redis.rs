use redis::{AsyncCommands, Client};
use url::Url;
use tracing::info;

pub async fn get_redis_client(redis_url: &str) -> Result<Client, Box<dyn std::error::Error>> {
    let url = Url::parse(redis_url)?;
    
    if url.scheme() == "redis" {
        let client = Client::open(redis_url)?;
        Ok(client)
    } else if url.scheme() == "sentinel" {
        // Rust's redis crate handles sentinels differently.
        // For simplicity in this refactor, I'll assume standard redis for now
        // but note that a full implementation would use redis::sentinel::Sentinel.
        // The original python code has a complex sentinel setup.
        Err("Sentinel scheme not fully implemented in this refactor yet".into())
    } else {
        Err("Invalid Redis URL scheme".into())
    }
}

pub async fn get_list_len(redis_url: &str, key: &str) -> Result<u64, Box<dyn std::error::Error>> {
    let client = get_redis_client(redis_url).await?;
    let mut conn = client.get_multiplexed_async_connection().await?;
    
    info!("start list_len: {}", key);
    let len: u64 = conn.llen(key).await?;
    info!("end list_len: {}", key);
    
    Ok(len)
}

pub async fn get_hash_len(redis_url: &str, key: &str) -> Result<u64, Box<dyn std::error::Error>> {
    let client = get_redis_client(redis_url).await?;
    let mut conn = client.get_multiplexed_async_connection().await?;
    
    info!("start hlen: {}", key);
    let len: u64 = conn.hlen(key).await?;
    info!("end hlen: {}", key);
    
    Ok(len)
}
