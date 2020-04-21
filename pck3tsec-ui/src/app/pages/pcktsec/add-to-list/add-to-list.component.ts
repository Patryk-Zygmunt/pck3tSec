import {Component, Input, OnInit} from '@angular/core';
import {NbDialogRef} from "@nebular/theme";
import {Host, HostList} from "../../../_model/model";
import {HostsService} from "../../../_service/hosts.service";

@Component({
  selector: 'ngx-add-to-list',
  templateUrl: './add-to-list.component.html',
  styleUrls: ['./add-to-list.component.scss']
})
export class AddToListComponent {



  @Input() host: any;
  reason:string;

  constructor(protected ref: NbDialogRef<AddToListComponent>,private hostService:HostsService) {}



  addToBlackList(){
    this.host.reason = this.reason;
    console.log(this.host)
    this.hostService.addToBlackList(this.host)
      .subscribe(()=>this.ref.close())
  }


  addToWhiteList(){
    this.host.reason = this.reason;
    this.hostService.addToWhiteList(this.host)
      .subscribe(()=>this.ref.close())
  }



}
