import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { flaskLink } from './link';

@Injectable({
  providedIn: 'root'
})
export class ExamService {

 
  private baseUrlPrin = flaskLink._API;

  private baseUrl = this.baseUrlPrin + 'verifica';

  constructor(private http: HttpClient) { }

  getVerifica(id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/${id}`);
  }
  

  createVerifica(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}`, user);
  }

  updateVerifica(id: string, value: any): Observable<Object> {
    return this.http.put(`${this.baseUrl}/${id}`, value);
  }

  deleteVerifica(id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`, { responseType: 'text' });
  }

  getVerificaList(): Observable<any> {
    return this.http.get(`${this.baseUrl}`);
  }

}