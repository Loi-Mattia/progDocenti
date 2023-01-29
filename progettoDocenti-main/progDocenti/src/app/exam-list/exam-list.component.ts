import { Observable } from "rxjs";
import { ExamService } from "../exam.service";
import { Exam } from "../exam";
import { Component, OnInit } from "@angular/core";
import { Router } from '@angular/router';
import {Location} from '@angular/common'

@Component({
  selector: 'app-exam-list',
  templateUrl: './exam-list.component.html',
  styleUrls: ['./exam-list.component.css']
})
export class ExamListComponent implements OnInit {
  data: Exam[] = undefined!;
  obsRooms: Observable<Exam[]> | undefined
  t: any;

  constructor(private userService: ExamService, private router: Router,private location: Location ) { }

  ngOnInit() {
    this.reloadData();
  }

  reloadData() {
    this.obsRooms = this.userService.getVerificaList()
    this.obsRooms.subscribe(this.fati)
  }
  fati = (data: Exam[]) => {
    this.data = data;
  }


  deleteVerifica(id: string) {
    this.userService.deleteVerifica(id)
      .subscribe(
        data => {
          console.log(data);
          this.reloadData();
        },
        error => console.log(error));
  }
  updateVerifica(id: string) {
    this.router.navigate(['updateVerifica', id]);
  }
  logout()  {
    // Clear session data
    this.t = localStorage.removeItem('user');
    this.router.navigate(['/login']);
    console.log("hjhjhjhjhjhjkhjkh"+this.t);
  }
}