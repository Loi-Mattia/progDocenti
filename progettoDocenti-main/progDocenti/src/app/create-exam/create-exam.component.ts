import { ExamService } from '../exam.service';
import { Exam } from '../exam';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {Location} from '@angular/common'

@Component({
  selector: 'app-create-exam',
  templateUrl: './create-exam.component.html',
  styleUrls: ['./create-exam.component.css']
})
export class CreateExamComponent implements OnInit{
  user: Exam = new Exam();
  submitted = false;

  constructor(private userService: ExamService,
    private router: Router,private location: Location ) { }

  ngOnInit() {
  }

  newUser(): void {
    this.submitted = false;
    this.user = new Exam();
  }

  save() {
    this.userService
    .createVerifica(this.user).subscribe(data => {
      console.log(data)
      this.user = new Exam();
      this.gotoList();
    }, 
    error => console.log(error));
  }

  onSubmit() {
    this.submitted = true;
    this.save();    
  }

  gotoList() {
    this.router.navigate(['/verifica']);
  }

  back() : void
  {
    this.location.back();
  }
}
