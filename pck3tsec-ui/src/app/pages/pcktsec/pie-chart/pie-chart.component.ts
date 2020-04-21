import { Component, OnInit } from '@angular/core';
import {NbThemeService} from "@nebular/theme";

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

  constructor(private theme: NbThemeService) {
    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      const colors: any = config.variables;
      const chartjs: any = config.variables.chartjs;

      this.data = {
        labels: ['Safe traffic', 'Threats', 'Blocked'],
        datasets: [{
          data: [300, 500, 100],
          backgroundColor: [colors.successLight, colors.warningLight, colors.dangerLight],
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
    });
  }

  ngOnDestroy(): void {
    this.themeSubscription.unsubscribe();
  }
}
