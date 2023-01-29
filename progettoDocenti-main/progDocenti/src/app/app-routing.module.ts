import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateExamComponent } from './create-exam/create-exam.component';

import { ExamListComponent } from './exam-list/exam-list.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { UpdateExamComponent } from './update-exam/update-exam.component';

const routes: Routes = [ 
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'verifica', component: ExamListComponent },
  { path: 'addVerifica', component: CreateExamComponent },
  { path: 'updateVerifica/:id', component: UpdateExamComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
