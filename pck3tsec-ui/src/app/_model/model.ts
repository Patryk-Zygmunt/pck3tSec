export interface HostList {
  id: number;
  host: string;
  reason: string;
  time_added: Date;
}

export interface Host {
  id: number;
  fqd_name: string;
  blocked: boolean;
  original_ip: string;
  threat: boolean;
  created_at:Date;
}

export interface Threat {
  id: number;
  host_source: Host
  http_path: string;
  threat_type: string;
  threat_details: any;
  discovered: Date;

}
