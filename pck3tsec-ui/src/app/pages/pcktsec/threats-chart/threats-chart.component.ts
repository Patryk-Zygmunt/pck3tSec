import { Component, OnInit } from '@angular/core';
import {NbColorHelper, NbThemeService} from '@nebular/theme';

@Component({
  selector: 'ngx-threats-chart',
  template: `
    <chart type="line" [data]="data" [options]="options"></chart>
  `,
  styleUrls: ['./threats-chart.component.scss'],
})
export class ThreatsChartComponent implements OnInit {

  data: any;
  options: any;

  constructor(private theme: NbThemeService) { }

  ngOnInit(): void {
     this.theme.getJsTheme().subscribe(config => {
      const colors: any = config.variables;
      const chartjs: any = config.variables.chartjs;


    this.data = {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [{
        data: [65, 59, 80, 81, 56, 55, 40],
        label: 'Detected threats',
        backgroundColor: NbColorHelper.hexToRgbA(colors.danger, 0.3),
        borderColor: colors.primary,
      }],
    };

       this.options = {
         responsive: true,
         maintainAspectRatio: false,
         scales: {
           xAxes: [
             {
               gridLines: {
                 display: true,
                 color: chartjs.axisLineColor,
               },
               ticks: {
                 fontColor: chartjs.textColor,
               },
             },
           ],
           yAxes: [
             {
               gridLines: {
                 display: true,
                 color: chartjs.axisLineColor,
               },
               ticks: {
                 fontColor: chartjs.textColor,
               },
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

}
