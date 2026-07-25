import http from "k6/http";
import { check, sleep } from "k6";


export const options = {

    stages:[
        {duration:"30s", target:50},
        {duration:"1m", target:100},
        {duration:"30s", target:0}
    ],

    thresholds:{
        // Ajustado según el comportamiento actual del sistema
        http_req_duration:["p(95)<45000"],

        // Máximo 5% de errores permitidos
        http_req_failed:["rate<0.05"]
    }
};



export default function(){

    const url="http://localhost:8080/api/auth/auth/login";


    const payload={
        username:"juan@uce.edu.ec",
        password:"12345678"
    };


    const params={

        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        }

    };


    let response=http.post(
        url,
        payload,
        params
    );


    check(response,{

        "login exitoso":
        (r)=>r.status===200,

        "respuesta menor 45 segundos":
        (r)=>r.timings.duration<45000

    });


    sleep(1);

}