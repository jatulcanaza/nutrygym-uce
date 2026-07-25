import http from "k6/http";
import { check, sleep } from "k6";

export const options = {

    stages: [

        {
            duration: "30s",
            target: 20
        },

        {
            duration: "1m",
            target: 100
        },

        {
            duration: "30s",
            target: 0
        }

    ],

    thresholds: {

        http_req_duration: [
            "p(95)<30000"
        ],

        http_req_failed: [
            "rate<0.05"
        ]

    }

};


// ======================
// LOGIN UNA SOLA VEZ
// ======================

export function setup() {

    const login = http.post(

        "http://localhost:8080/api/auth/auth/login",

        {
            username: "juan@uce.edu.ec",
            password: "12345678"
        },

        {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }

    );

    check(login, {
        "login correcto": (r) => r.status === 200
    });

    return {
        token: login.json("access_token")
    };

}


// ======================
// PRUEBA
// ======================

export default function (data) {

    const response = http.get(

        "http://localhost:8080/api/plans/plans/current",

        {

            headers: {
                Authorization: `Bearer ${data.token}`
            }

        }

    );

    check(response, {

        "consulta correcta":
            (r) => r.status === 200,

        "respuesta menor 30 segundos":
            (r) => r.timings.duration < 30000

    });

    sleep(1);

}