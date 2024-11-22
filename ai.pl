:- use_module(library(csv)).
:- use_module(library(http/http_server)).
:- use_module(library(http/http_parameters)).

:- dynamic student/4.

load_data(File) :-
    retractall(student(_, _, _, _)),
    csv_read_file(File, Rows, [functor(student), arity(4)]),
    maplist(assert, Rows).

is_scholarship_eligible(StudentID) :-
    student(StudentID, _, Attendance, CGPA),
    Attendance >= 75,
    CGPA >= 9.0.

is_exam_permitted(StudentID) :-
    student(StudentID, _, Attendance, _),
    Attendance >= 75.

:- http_handler(root(eligibility), process_request, []).

process_request(Request) :-
    ( http_parameters(Request, [id(StudentID, [integer])]) ->
        ( student(StudentID, Name, Attendance, CGPA) ->
            ( is_scholarship_eligible(StudentID) ->
                Status = "Eligible for exam"
            ; is_exam_permitted(StudentID) ->
                Status = "Eligible for Exam Only"
            ; Status = "Not Eligible"
            ),
            format('Content-type: text/plain~n~n'),
            format('Student ID: ~w (~w), Attendance: ~w, CGPA: ~w, Status: ~w~n',
                   [StudentID, Name, Attendance, CGPA, Status])
        )
    ; 
        findall([ID, Name, Attendance, CGPA, Status],
                ( student(ID, Name, Attendance, CGPA),
                  ( is_scholarship_eligible(ID) ->
                      Status = "Eligible for Scholarship and Exam"
                  ; is_exam_permitted(ID) ->
                      Status = "Eligible for Exam Only"
                  ; Status = "Not Eligible"
                  )
                ),
                Results),
        format('Content-type: text/plain~n~n'),
        print_all_results(Results)
    ).

print_all_results([]).
print_all_results([[ID, Name, Attendance, CGPA, Status] | Rest]) :-
    format('Student ID: ~w (~w), Attendance: ~w, CGPA: ~w, Status: ~w~n',
           [ID, Name, Attendance, CGPA, Status]),
    print_all_results(Rest).
