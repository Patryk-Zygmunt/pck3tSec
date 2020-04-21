import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddToListComponent } from './add-to-list.component';

describe('AddToListComponent', () => {
  let component: AddToListComponent;
  let fixture: ComponentFixture<AddToListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddToListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddToListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
