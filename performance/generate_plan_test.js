import http from "k6/http";
import { check, sleep } from "k6";


export const options = {

    stages:[
        {
            duration:"30s",
            target:20
        },
        {
            duration:"1m",
            target:50
        },
        {
            duration:"30s",
            target:0
        }
    ],


    thresholds:{

        http_req_duration:[
            "p(95)<30000"
        ],

        http_req_failed:[
            "rate<0.05"
        ]

    }

};



export default function(){


    // =====================================
    // 1. LOGIN
    // =====================================

    const loginResponse = http.post(

        "http://localhost:8080/api/auth/auth/login",

        {
            username:"juan@uce.edu.ec",
            password:"12345678"
        },

        {
            headers:{
                "Content-Type":
                "application/x-www-form-urlencoded"
            }
        }

    );


    check(loginResponse,{

        "login correcto":
        (r)=>r.status===200

    });


    const token = loginResponse.json("access_token");



    // =====================================
    // 2. DATOS DEL PERFIL NUTRICIONAL
    // =====================================


    const payload = JSON.stringify({

    user_id:"2a7a45bf-dba9-4076-a008-1a4bc4593da6",

    age:22,

    weight:75,

    height:175,

    gender:"Male",

    activity:"Moderate",

    goal:"Gain muscle",

    preferences:"High protein",

    allergies:"None",

    meals:4,

    diet:"Medium",

    calories:2200,

    water:2.5,

    protein:150,

    carbs:250,

    fats:70

    });


    // =====================================
    // 3. GENERAR PLAN
    // =====================================


    const response = http.post(

        "http://localhost:8080/api/plans/plans",

        payload,

        {

            headers:{

                "Content-Type":
                "application/json",

                "Authorization":
                `Bearer ${token}`

            }

        }

    );



    if(response.status !== 200 && response.status !== 201){

    console.log(
        "ERROR:",
        response.body
    );

}



    check(response,{

    "plan generado":
    (r)=>r.status===200 || r.status===201,


    "respuesta IA aceptable":
    (r)=>r.timings.duration < 30000

    });



    sleep(2);

}