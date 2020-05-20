import { Component, OnInit } from '@angular/core';
import {NbThemeService} from "@nebular/theme";
import {HostsService} from "../../../_service/hosts.service";

@Component({
  selector: 'ngx-pie-chart',
  template: `
    <chart type="pie" [data]="data" [options]="options"></chart>
  `,
  styleUrls: ['./pie-chart.component.scss']
})
export class PieChartComponent {

  data: any;
  options: any;
  themeSubscription: any;

  constructor(private theme: NbThemeService,private hostService:HostsService) {
    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      this.hostService.getHosts().subscribe(res=>{
        let threat = res.filter(r=>r.threat).length
        let nthreat = res.filter(r=>!r.threat).length


        const colors: any = config.variables;
        const chartjs: any = config.variables.chartjs;

        this.data = {
          labels: ['Safe traffic', 'Threats'],
          datasets: [{
            data: [nthreat, threat],
            backgroundColor: [colors.successLight, colors.warningLight],
          }],
        };

        this.options = {
          maintainAspectRatio: false,
          responsive: true,
          scales: {
            xAxes: [
              {
                display: false,
              },
            ],
            yAxes: [
              {
                display: false,
              },
            ],
          },
          legend: {
            labels: {
              fontColor: chartjs.textColor,
            },
          },
        };
      })

    });
  }

  ngOnDestroy(): void {
    this.themeSubscription.unsubscribe();
  }
}
