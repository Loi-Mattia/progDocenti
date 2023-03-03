import { Component, OnInit } from '@angular/core';
import { Exam } from '../exam';
import { ActivatedRoute, Router } from '@angular/router';
import { ExamService } from '../exam.service';

@Component({
  selector: 'app-update-exam',
  templateUrl: './update-exam.component.html',
  styleUrls: ['./update-exam.component.css']
})
export class UpdateExamComponent implements OnInit {

  id: string = "";
  user: Exam = undefined!;

  constructor(private route: ActivatedRoute,private router: Router, private userService: ExamService) { }

  ngOnInit() {
    this.user = new Exam();
    this.id = this.route.snapshot.params['id'];
    console.log("id: "+this.id)
    this.userService.getVerifica(this.id)
      .subscribe(data => {
        this.user = data;
      }, error => console.log(error));
      console.log(this.userService);
  }

  updateVerifica() {
    this.userService.updateVerifica(this.id, this.user)
      .subscribe(data => {
        console.log(data);
        this.user = new Exam();
        this.gotoList();
      }, error => console.log(error));
  }

  

  onSubmit() {
    console.log("onSubmit")
    this.updateVerifica();     
  }

  gotoList() {
    this.router.navigate(['/verifica']);
  }
}