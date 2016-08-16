function showNavLinks() {
    $(".nav").empty();
    $(".nav").append($("<li><button class='btn'>Sessions</button></li>")
        .attr("role", "presentation")
        .attr("id", "sess-link"));
    $(".nav").append($("<li><button class='btn'>Courses</button></li>")
        .attr("role", "presentation")
        .attr("id", "crs-link"));
    $(".nav").append($("<li><button class='btn'>Patients</button></li>")
        .attr("role", "presentation")
        .attr("id", "pat-link"));
    $(".nav").append($("<li><button class='btn'>Instructors</button></li>")
        .attr("role", "presentation")
        .attr("id", "instr-link"));
    $("#sess-link").click(function() {
        page("/");    
    });
    $("#crs-link").click(function() {
        page('/courses');    
    });
    $("#instr-link").click(function() {
        page("/instructors");    
    });
    $("#pat-link").click(function() {
        page("/patients");
    });   
}

function showPatients() {
    $.get("/api/patients")
        .done(function(data) {
            populatePatientsTable(data.patients)
        });
}

function populatePatientsTable(patients) {
    $("#page-specific").empty();
    showNavLinks();
    $("#page-specific").append("<h2>Patients</h2>");
    $("#page-specific")
        .append($(" <button>Add patient</button>")
        .addClass("btn btn-default")
        .attr("type", "button")
        .attr("id", "add-patient"));
    $("#add-patient").click(function() {
        addPatientForm();
    });
    if (patients[0]) {
        var table = $("<table>")
            .addClass("table table-bordered").attr("id", "patients-table");
        var thead = $("<thead>");
        var tr = $("<tr>");
        tr.append($("<th>Patient ID</th>"));
        tr.append($("<th>Patient code</th>"));
        tr.append($("<th>Options</th>"));
        thead.append(tr);
        table.append(thead);
        table.append($("<tbody>"));
        $("#page-specific").append(table);
        $.each(patients, function(index, patient) {
            var row = $("<tr>");
            row.append($("<td>").text(patient.id));
            row.append($("<td>").text(patient.code));
            var editButton = $("<button>Edit</button>")
                .addClass("btn btn-default")
                .attr("id","edit" + patient.id);
            row.append(editButton);
            editButton.click(function() {
                editPatientForm(patient.id);            
            });            
            $("#patients-table tbody").append(row);
        });
    } else {
        $("#page-specific").append("<h3>No patients available</h3>");
    }   
}

function addPatientForm() {
    $("#page-specific").empty();
    showNavLinks();
    $("#page-specific").append("<h2>Add patient</h2>");
    var source = $("#patient-form-template").html();
    var template = Handlebars.compile(source);        
    $("#page-specific").append(template());
    $("#patient-form").submit(function() {
        $("form button").prop("disabled", true);
        var code = $("#patientCode").val();
        $.post("/api/patients", {code: code});
        return false;
    });
}

function editPatientForm(id) {
    $.get("/api/patients/" + id)
        .done(function(data) {
            patient = data;    
            $("#page-specific").empty();
            showNavLinks();
            $("#page-specific").append("<h2>Edit patient</h2>");
            var source = $("#patient-form-template").html();
            var template = Handlebars.compile(source);        
            $("#page-specific").append(template(patient));
            $("#patient-form").submit(function() {
                $("form button").prop("disabled", true);
                var code = $("#patientCode").val();
                $.post("/api/patients/" + id, {code: code});
                return false;
            });
        });
}

function showInstructors() {
    $.get("/api/instructors")
        .done(function(data) {            
            populateInstructorsTable(data.instructors);
        });
}

function populateInstructorsTable(instructors) {
    $("#page-specific").empty();
    showNavLinks();
    $("#page-specific").append("<h2>Instructors</h2>");
    $("#page-specific")
        .append($(" <button>Add instructor</button>")
        .addClass("btn btn-default")
        .attr("type", "button")
        .attr("id", "add-instructor"));
    $("#add-instructor").click(function() {
        addInstructorForm();
    });
    if (instructors[0]) {
        var table = $("<table>")
            .addClass("table table-bordered").attr("id", "instructors-table");
        var thead = $("<thead>");
        var tr = $("<tr>");
        tr.append($("<th>Instructor ID</th>"));
        tr.append($("<th>Name</th>"));
        tr.append($("<th>Email</th>"));
        tr.append($("<th>Options</th>"));
        thead.append(tr);
        table.append(thead);
        table.append($("<tbody>"));
        $("#page-specific").append(table);
        $.each(instructors, function(index, instructor) {
            var row = $("<tr>");
            row.append($("<td>").text(instructor.id));
            row.append($("<td>").text(instructor.name));
            row.append($("<td>").text(instructor.email));
            var editButton = $("<button>Edit</button>")
                .addClass("btn btn-default")
                .attr("id","edit" + instructor.id);
            row.append(editButton);
            editButton.click(function() {
                editInstructorForm(instructor.id);            
            });            
            $("#instructors-table tbody").append(row);
        });
    } else {
        $("#page-specific").append("<h3>No instructors available</h3>");
    }   
            

}

function addInstructorForm() {
    $("#page-specific").empty();
    showNavLinks();
    $("#page-specific").append("<h2>Add instructor</h2>");
    var source = $("#instructor-form-template").html();
    var template = Handlebars.compile(source);        
    $("#page-specific").append(template());
    $("#instructor-form").submit(function() {
        $("form button").prop("disabled", true);
        var name = $("#instructorName").val();
        var email = $("#instructorEmail").val();
        $.post("/api/instructors", {name: name, email: email});
        return false;
    });
}

function editInstructorForm(id) {
    $.get("/api/instructors/" + id)
        .done(function(data) {
            instructor = data;    
            $("#page-specific").empty();
            showNavLinks();
            $("#page-specific").append("<h2>Edit instructor</h2>");
            var source = $("#instructor-form-template").html();
            var template = Handlebars.compile(source);        
            $("#page-specific").append(template(instructor));
            $("#instructor-form").submit(function() {
                $("form button").prop("disabled", true);
                var name = $("#instructorName").val();
                var email = $("#instructorEmail").val();
                $.post("/api/instructors/" + id, {name: name, email: email});
                return false;
            });
        });
}

function showCourses() {
    $.get("/api/courses")
        .done(function(data) {
            populateCoursesTable(data.courses);        
        });
}

function populateCoursesTable(courses) {
    $("#page-specific").empty();
    showNavLinks();
    $("#page-specific").append("<h2>Courses</h2>");
    $("#page-specific")
        .append($(" <button>Add course</button>")
        .addClass("btn btn-default")
        .attr("type", "button")
        .attr("id", "add-course"));
    $("#add-course").click(function() {
        addCourseForm();
    });
    if (courses[0]) {
        var table = $("<table>")
            .addClass("table table-bordered").attr("id", "courses-table");
        var thead = $("<thead>");
        var tr = $("<tr>");
        tr.append($("<th>Course ID</th>"));
        tr.append($("<th>Instructor ID</th>"));
        tr.append($("<th>Name</th>"));
        tr.append($("<th>Code</th>"));
        tr.append($("<th>Credit Value</th>"));
        tr.append($("<th>Options</th>"));
        thead.append(tr);
        table.append(thead);
        table.append($("<tbody>"));
        $("#page-specific").append(table);
        $.each(courses, function(index, course) {
            var row = $("<tr>");
            row.append($("<td>").text(course.id));
            row.append($("<td>").text(course.instructor_id));
            row.append($("<td>").text(course.name));
            row.append($("<td>").text(course.code));
            row.append($("<td>").text(course.credit_value));
            var editButton = $("<button>Edit</button>")
                .addClass("btn btn-default")
                .attr("id","edit" + course.id);
            row.append(editButton);
            editButton.click(function() {
                editCourseForm(course.id);            
            });            
            $("#courses-table tbody").append(row);
        });
    } else {
        $("#page-specific").append("<h3>No courses available</h3>");
    }   
}

function addCourseForm() {
    $("#page-specific").empty();
    showNavLinks();
    $("#page-specific").append("<h2>Add course</h2>");
    $.get("/api/instructors")
        .done(function(data) {
            var source   = $("#course-form-template").html();
            var template = Handlebars.compile(source);        
            $("#page-specific").append(template(data));
            $("#course-form").submit(function() {
                $("form button").prop("disabled", true);
                var name = $("#courseName").val();
                var instructor_id = $("#courseInstructor").val();
                var code = $("#courseCode").val();
                var credits = $("#courseCredits").val();
                $.post("/api/courses", {
                    name: name, 
                    instructor_id: instructor_id, 
                    code: code, 
                    credits: credits
                    });
                return false;
            });
        });
}

function editCourseForm(id) {
    $.get("/api/courses/" + id)
        .done(function(course) {
            $.get("/api/instructors")
                .done(function(instructors) {
                    $("#page-specific").empty();
                    showNavLinks();
                    $("#page-specific").append("<h2>Edit course</h2>");
                    var source = $("#course-form-template").html();
                    var template = Handlebars.compile(source);  
                    data = {course: course, instructors: instructors};    
                    $("#page-specific").append(template(data)); 
                    $("#course-form").submit(function() {
                        var name = $("#courseName").val();
                        var instructor_id = $("#courseInstructor").val();
                        var code = $("#courseCode").val();
                        var credits = $("#courseCredits").val();
                        $.post("/api/courses", {
                            name: name, 
                            instructor_id: instructor_id, 
                            code: code, 
                            credits: credits
                        });
                        return false;
                    });
                });    
        });
}

function showSessions() {
    $.get("/api/sessions")
        .done(function(data) {
            populateSessionsTable(data.sessions);
        });
}

function populateSessionsTable(sessions) {
    $("#page-specific").empty();
    showNavLinks();
    $("#page-specific").append("<h2>Recorded Sessions</h2>");
    var table = $("<table>")
        .addClass("table table-bordered").attr("id", "sessions-table");
    var thead = $("<thead>");
    var tr = $("<tr>");
    tr.append($("<th>Session ID</th>"));
    tr.append($("<th>Start time</th>"));
    tr.append($("<th>End time</th>"));
    tr.append($("<th>Course ID</th>"));
    tr.append($("<th>Patient ID</th>"));
    tr.append($("<th>Sample rate</th>"));
    tr.append($("<th>Measurement resolution</th>"));
    thead.append(tr);
    table.append(thead);
    table.append($("<tbody>"));
    $("#page-specific").append(table);
    $.each(sessions, function(index, session) {
        var row = $("<tr>");
        row.append($("<td>").text(session.id));
        row.append($("<td>").text(session.start_time));
        row.append($("<td>").text(session.end_time));
        row.append($("<td>").text(session.course_id));
        row.append($("<td>").text(session.patient_id));
        row.append($("<td>").text(session.sample_rate + " Hz"));
        row.append($("<td>").text(session.resolution));
        row.click(function() {
            page("/sessions/" + session.id);
        });       
        $("#sessions-table tbody").append(row);
    });
}

function showSamples(ctx) {
    var id = ctx.params.id;
    $.get("/api/sessions/" + id + "/samples")
        .done(function(data) {
           populateSamplesTable(data.samples);        
        });
}

function populateSamplesTable(samples) {
    $("#page-specific").empty();
    showNavLinks();
    $("#page-specific").append("<h2>Recorded Samples</h2>");
    $("#page-specific")
        .append($(" <button>Back to Sessions list</button>")
        .addClass("btn btn-default")
        .attr("type", "button")
        .attr("id", "back"));
    $("#back").click(function() {
        page("/");    
    });
    createSampleChart(samples, 0);
    createSampleChart(samples, 1);
    createSampleChart(samples, 2);
    createSampleChart(samples, 3);
    createSampleChart(samples, 4);
    createSampleChart(samples, 5);
    createSampleChart(samples, 6);
    createSampleChart(samples, 7);
}

function createSampleChart(samples, channel) {    
    $("#page-specific").append($("<canvas>")
        .attr("id","sample-chart" + channel)); 
    var canvas = $("#sample-chart" + channel);
    var sampleArray = []    
    $.each(samples, function(index, sample) {
        sampleTime = sample.order_number * 0.004;
        sampleVoltage = sample.channel_data[channel];
        sampleArray[index] = {
            x: sampleTime,
            y: sampleVoltage
        };
    });
    var chart = new Chart(canvas, {
        type: "line",
        data: {
            datasets:[{
                fill: false,
                data: sampleArray,
                radius: 0,
                tension: 0,
                borderColor: "rgba(0,0,0,1)",
                borderWidth: 1,
            }]        
        },
        options: {
            legend: {
                display: false            
            },
            title: {
                display: true, 
                text: "Channel " + (channel + 1)            
            },
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom',
                    scaleLabel: {
                        display:true,
                        labelString: "Time (seconds)"
                    }
                }],
                yAxes: [{
                    type: "linear",
                    scaleLabel: {
                        display:true,
                        labelString: "Voltage (microvolts)"                    
                    }    
                }]
            },
            
        }      
    });    
}


page('/', showSessions);
page('/sessions/:id', showSamples);
page('/courses', showCourses);
page('/instructors', showInstructors);
page('/patients', showPatients);

page({"hashbang": true});

