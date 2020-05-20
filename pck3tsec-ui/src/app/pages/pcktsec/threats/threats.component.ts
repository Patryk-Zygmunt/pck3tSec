import {Component, Input, OnInit} from '@angular/core';
import {PcktsecListComponent} from "../pcktsec-list";
import {Host, Threat} from "../../../_model/model";
import {HostsService} from "../../../_service/hosts.service";
import {NbDialogService} from "@nebular/theme";

@Component({
  selector: 'ngx-threats',
  templateUrl: './threats.component.html',
  styleUrls: ['./threats.component.scss']
})
export class ThreatsComponent extends PcktsecListComponent implements OnInit {
  threats: Threat[] = []
  @Input()
  smallSize = 'large'


  constructor(protected  hostService: HostsService, protected dialogService: NbDialogService) {
    super(hostService, dialogService);
  }

  ngOnInit(): void {
    this.hostService.getThreats()
      .subscribe(res =>{
        //res.forEach(r=>r.threat_details = JSON.parse(r.threat_details) )
        this.threats = res

      })
  }
}
