export interface HostList {
  id: number;
  host: string;
  reason: string;
  time: Date;
}

export interface Host {
  id: number;
  host: string;
  blocked: boolean;
  ip: string;
  threat: boolean;
}

export interface Threat {
  id: number;
  host: string;
  type: string;
  details: string;
  threat: boolean;
  detected: Date;
  blocked: boolean;

}
