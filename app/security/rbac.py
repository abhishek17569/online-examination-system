GET = "GET"
POST = "POST"
PATCH = "PATCH"
DELETE = "DELETE"
admin = "admin"
student = "student"

rbac_rules = {
    "/api/v1/questions/": {
        POST: {admin: {}},
        GET: {admin: {}, student: {}},
    },
    "/api/v1/exams/": {
        POST: {admin: {}},
        GET: {admin: {}, student: {}},
    },
    "/api/v1/exams/<exam_id>": {
        GET: {admin: {}, student: {}},
    },
    "/api/v1/submissions/": {
        POST: {admin: {}, student: {}},
        GET: {admin: {}, student: {}},
    },
    "/api/v1/submissions/<submission_id>": {
        GET: {admin: {}, student: {}},
    },
    "/api/v1/results/": {
        GET: {student: {}},
    },
}
