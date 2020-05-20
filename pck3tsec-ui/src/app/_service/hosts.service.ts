import { Injectable } from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Host, HostList, Threat} from "../_model/model";

@Injectable({
  providedIn: 'root'
})
export class HostsService {
  private readonly URL = environment.url;



  constructor(private http: HttpClient) {
  }

  getHosts() {
    return  this.http.get<Host[]>(this.URL + '/hosts')
  }

  getThreats() {
    return  this.http.get<Threat[]>(this.URL + '/threats')
  }

  getWhiteList() {
    return  this.http.get<HostList[]>(this.URL + '/whitelist')
  }

  getBlackList() {
    return  this.http.get<HostList[]>(this.URL + '/blacklist')
  }

  addToBlackList(host) {
    return  this.http.post(this.URL + '/blacklist/',host)
  }

  addToWhiteList(host) {
    return  this.http.post(this.URL + '/whitelist/',host)
  }

  deleteFromBlacklist(hostId: any) {
    return  this.http.delete(this.URL + '/blacklist/'+hostId)
  }

  deleteFromWhitelist(hostId: any) {
    return  this.http.delete(this.URL + '/whitelist/'+hostId)
  }


}
