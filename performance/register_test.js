import http from "k6/http";
import { check, sleep } from "k6";


export const options = {

    vus:100,

    duration:"1m",

    thresholds:{
        http_req_duration:[
            "p(95)<45000"
        ],

        http_req_failed:[
            "rate<0.05"
        ]
    }

};



export default function(){

    const random = Math.floor(Math.random()*1000000);


    const payload = JSON.stringify({

        name:
        "Usuario Test " + random,

        email:
        `usuario${random}@uce.edu.ec`,

        password:
        "12345678"

    });



    let res = http.post(

        "http://localhost:8080/api/auth/auth/register",

        payload,

        {

            headers:{
                "Content-Type":"application/json"
            }

        }

    );


    check(res,{

        "registro creado":
        (r)=>r.status===201 || r.status===200,

        "respuesta menor 45 segundos":
        (r)=>r.timings.duration < 45000

    });


    sleep(1);

}