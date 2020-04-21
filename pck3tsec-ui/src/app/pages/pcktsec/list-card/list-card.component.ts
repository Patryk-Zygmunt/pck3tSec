import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'ngx-list-card',
  templateUrl: './list-card.component.html',
  styleUrls: ['./list-card.component.scss']
})
export class ListCardComponent implements OnInit {
  @Input() title: string;
  @Input() type: string;
  @Input() on = true;
  @Input() onOff = true;
  @Input() icon: string;

  constructor() { }

  ngOnInit(): void {
  }


  changeState() {
    if(this.onOff) {this.on = !this.on}
  }
}
