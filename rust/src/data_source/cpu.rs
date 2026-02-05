use sysinfo::System;

pub fn get_cpu_usage() -> f32 {
    let mut sys = System::new_all();
    sys.refresh_cpu_usage();
    // In sysinfo, we need to wait a small bit or refresh twice to get accurate usage
    std::thread::sleep(sysinfo::MINIMUM_CPU_UPDATE_INTERVAL);
    sys.refresh_cpu_usage();
    
    let cpus = sys.cpus();
    if cpus.is_empty() {
        return 0.0;
    }
    
    let total_usage: f32 = cpus.iter().map(|cpu| cpu.cpu_usage()).sum();
    total_usage / cpus.len() as f32
}
