use sysinfo::System;

pub fn get_memory_usage() -> f32 {
    let mut sys = System::new_all();
    sys.refresh_memory();
    
    let total = sys.total_memory() as f32;
    let used = sys.used_memory() as f32;
    
    if total == 0.0 {
        return 0.0;
    }
    
    (used / total * 10000.0).round() / 10000.0
}
