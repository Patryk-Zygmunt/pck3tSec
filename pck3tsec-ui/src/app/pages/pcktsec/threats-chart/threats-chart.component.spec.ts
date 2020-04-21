import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ThreatsChartComponent } from './threats-chart.component';

describe('ThreatsChartComponent', () => {
  let component: ThreatsChartComponent;
  let fixture: ComponentFixture<ThreatsChartComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ThreatsChartComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ThreatsChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
