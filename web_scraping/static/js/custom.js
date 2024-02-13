let ec2_ip = '13.127.104.212:8000'
let placeholderImg = `http://${ec2_ip}/media/images/default.png`
let nullDataElement = null
let acceptedDataElement = null
let rejectedDataElement = null
let dataTable;
let legislative_dataTable;
let combine_dataTable;

$(document).ready(function () {
    // Initially display the loader when the page loads
    document.getElementById('loader').style.display = 'none';
});

$(document).ready(function () {
    var null_data_class = document.querySelector('.null_data');
    var accepted_data_class = document.querySelector('.accepted_data');
    var rejected_data_class = document.querySelector('.rejected_data');
    var legislative_data_class = document.querySelector('.legislative_data');
    var combine_data_class = document.querySelector('.combine_data');
    // var accepted_data_modification = document.querySelector('.accepted_data_modification');

    // Check if the element with the target class exists on the page
    if (null_data_class) {
        // Your code to run when the class is present on this page
        console.log('Null Data');
        initDataTable('null');
    }

    if (accepted_data_class) {
        // Your code to run when the class is present on this page
        console.log('Accepted Data');
        initDataTable('true');
    }
    
    if (rejected_data_class) {
        // Your code to run when the class is present on this page
        console.log('Rejected Data');
        initDataTable('false');

    }

    if (legislative_data_class) {
        // Your code to run when the class is present on this page
        console.log('Legislative Data');
        LegislativeDataTable();
    }

    if (combine_data_class) {
        // Your code to run when the class is present on this page
        console.log('Combine Data');
        CombineDataTable();
    }


    
    // if (accepted_data_modification) {
    //     // Your code to run when the class is present on this page
    //     console.log('Accepted Modification Data');
    //     initDataTable('true');

    // }
});

// Function to initialize DataTable
function initDataTable(validationStatus, modification) {

     // Destroy existing DataTable if it exists
     if (dataTable) {
        dataTable.destroy();
    }

    // Get CSRF token
    const csrftoken = getCookie('csrftoken');
    dataTable = $('#leadership-table').DataTable({
        "dom": '<"top"Bf<"clear">><"top"lip<"clear">>rt<"bottom"ip<"clear">>',
        // autoWidth: false,
        scrollX: true,
        serverSide: true,
        orderCellsTop: true,
        rowReorder: true,
        ajax: {
            url: `/get_data/?validation_status=${validationStatus}&modification=${modification}`,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
        },
        pageLength: 100,  // Set the number of records per page
        columns: [
            { data: 'id',  title: 'ID' },
            { data: 'image_name',title: 'Image', render: function (data, type, row) {
                const imageUrl = `https://gov-finder.s3.amazonaws.com/images/${data.replace(/\.(png|jpg|webp)$/, '')}.png`;
                return `<img style="width:80px;" src="${imageUrl}" onerror="this.src='${placeholderImg}'" />`;
            }},
            { data: 'name',  title: 'Name' },
            { data: 'designation',  title: 'Designation' },
            { data: 'dep',  title: 'Department' },
            { data: 'address',  title: 'Address' },
            { data: 'email',  title: 'Email' },
            { data: 'phone_number',  title: 'Phone' },
            {
                data: 'link',  title: 'Link',
                render: function (data, type, row) {
                    return `<a target="_blank" href="${data}">${data}</a>`;
                }
            },
            { data: 'desc',  title: 'Description' },
            {  data: 'hierarchy',  title: 'Hierarchy'},
            {
                data: 'validation',
                title: 'Status',
                render: function (data, type, row) {
                    if (row.validation === false) {
                        return `<p>Rejected</p>`;
                    } else if (row.validation === true) {
                        return `<p>Accepted</p>`;
                    } else {
                        return `<p>Unvalidated</p>`;
                    }
                },
                visible: false, // Set the default visibility here
            },

            
            
            {
                data: 'feedback_data',  title: 'Feedback',
                render: function (data, type, row) {
                    return `<textarea class="textarea" id="feedback_${row.id}">${data}</textarea> <button class="feedback_submit_btn btn btn-primary" data-id="${row.id}">Submit</button>`;
                }
            },
            {
                data: 'id',  title: 'Validation',
                render: function (data, type, row) {
                    if (row.validation === false) {
                        return `<button class="validate_accept submit_feedback btn btn-success" data-id="${data}">Accept</button>`;
                    } 
                    if (row.validation === true) {
                        return `<button class="validate_reject submit_feedback btn btn-danger" data-id="${data}">Reject</button>`;
                    }
                    else{
                        return `<span style = 'display: flex;'> <button style = 'margin:2px;' class="validate_accept submit_feedback btn btn-success" data-id="${data}">Accept</button>  <button style = 'margin:2px;' class="validate_reject submit_feedback btn btn-danger" data-id="${data}">Reject</button> </span> `;
                    }
                }
            },
        ],

        // Include the searchHighlight extension
        searchHighlight: true,
        search: {
            regex: true,  // Disable regular expression search
            smart: false,  // Disable smart search
            caseInsensitive: true  // Make the search case-insensitive
        },
        columnDefs: [
            {
                targets: 1,
                className: 'noVis'
            },
            {
                targets: [4],
                width: '200px'
            },
            {
                targets: [5],
                width: '300px'
            },
            {
                targets: [7],
                width: '200px'
            },
            {
                targets: [8],
                width: '300px',
                className:'link_class'
            },
            {
                targets: [9], 
                className: 'desc_class',
               
            },
            {
                targets: [10], 
                className: 'hierarchy_class',
                width: '200px',
            },
            { 
                orderable: true, 
                className: 'reorder', 
                targets: 0 },
            { 
                orderable: false, 
                targets: '_all' },
            { width: "400px", targets: 9 },
        ],
        buttons: [
            {
                extend: 'colvis',
                columns: ':not(.noVis)'
                
            },
            {
                extend: 'excel',
                text: 'Download File'
                // Add more buttons or options as needed
            }
        ],
        lengthMenu: [
            [ 100, 200, 500 ],
            [ '100', '200', '500']
        ],
        
        // Additional DataTable options can be added here
        
        initComplete: function() {
            dataTable.draw();
            applyDropdownFilter();
            
            
        }

        
    });

       // Add the draw event listener for search highlighting
       dataTable.on('draw', function () {
        console.log('DataTable initialized.');
        var body = $(dataTable.table().body());
        body.unhighlight();
        body.highlight(dataTable.search());
    });
}



// Function to apply dropdown filter
function applyDropdownFilter() {
    var dataTable = $('#leadership-table').DataTable();
    var column = dataTable.column(10);

    depart = ['Department of Veterans Affairs',
        'Executive Office of the President',
        'Department of Transportation',
        'Department of State',
        'Department of Treasury',
        'Department of Agriculture',
        'Department of Education',
        'Department of Energy',
        'Department of Commerce',
        'Department of Labour',
        'Department of Housing and Urban',
        'Department of Homeland Security',
        'Department of Justice',
        'Department of Health and Human Services',
        'Department of Interior',
        'Department of Defense',
        'Independent Establishment and Government Corporations'
    ];

    var select = $('<select><option value=""></option></select>')
        .appendTo($("thead tr").eq(0).find("th").eq(column.index()))
        .on('change', function() {
            // Get the selected value from the dropdown
            var dropdownValue = $.fn.dataTable.util.escapeRegex($(this).val());

            // Use a regular expression to match the exact value in the dropdown
            // var regex = '\\b' + dropdownValue + '\\b';

            // Set the search term for the specific column
            column
                .search(dropdownValue, true, false)
                .draw(); // Draw the table with the new search
        });

    depart.forEach(function(d) {
        select.append('<option value="' + d + '">' + d + '</option>');
    });
}


// Function to get CSRF token from cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).on('click', '.feedback_submit_btn', function () {
    const id = $(this).data('id');
    const feedbackText = $(`#feedback_${id}`).val();

    // Use your existing sendFeedback function
    sendFeedback(id, feedbackText, function () {
        console.log('Feedback submitted and data table updated for ID:', id);
    });
});

function sendFeedback(id, feedbackText, callback) {
    const url = `/feedback_data/${id}/`;
    const formData = new FormData();
    formData.append('feedback_data', feedbackText);

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.cookie.split('; ').find(c => c.startsWith('csrftoken')).split('=')[1],
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Feedback submitted successfully.');
            // Call the callback function to update the DataTable row
            callback();
        } else {
            console.log('Error: ' + data.errors);
        }
    })
    .catch(error => console.error('Error:', error));
}




// Use event delegation for dynamically added elements
$(document).on('click', '.validate_accept', function () {
    const id = $(this).data('id');
    // Retrieve the feedback text from the corresponding textarea
    const feedbackText = $(`#feedback_${id}`).val();
    handleValidation(id, true, feedbackText);
});

$(document).on('click', '.validate_reject', function () {
    const id = $(this).data('id');
    // Retrieve the feedback text from the corresponding textarea
    const feedbackText = $(`#feedback_${id}`).val();
    handleValidation(id, false, feedbackText);
});

let submittingFeedback = false;

function handleValidation(id, validation, feedbackText) {
    // If feedback is already being submitted, ignore the click
    if (submittingFeedback) {
        return;
    }

    // Send a GET request to validate or reject the data
    const url = validation ? '/accepted_data/' : '/rejected_data/';
    $.ajax({
        url: url,
        method: 'GET',
        data: { id: id },
        dataType: 'json',
        success: function (response) {
            console.log('Data Validated:', response);

            // Set the flag to indicate that feedback is being submitted
            submittingFeedback = true;

            // Hide the feedback box while feedback is being submitted
            const feedbackBox = $(`#feedback_${id}`);
            feedbackBox.hide();

            // Send feedback
            sendFeedback(id, feedbackText, function () {
                // Reset the flag after feedback is successfully submitted
                submittingFeedback = false;

                // After the DataTable row is successfully updated, show the feedback box
                feedbackBox.show();

                // Update the DataTable row
                const updatedRow = response.data;  // Define updatedRow in this scope
                updateDataTableRow(updatedRow);
            });
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('Error Validating Data:', errorThrown);
        },
    });
}

function updateDataTableRow(updatedRow) {
    const table = $('#leadership-table').DataTable();

    // Get all data in the DataTable
    const allData = table.rows().data().toArray();

    // Find the index of the row with the matching ID
    const rowIndex = allData.findIndex(row => row.id === updatedRow.id);

    if (rowIndex !== -1) {
        // If the row is found, update the data
        table.row(rowIndex).data(updatedRow).draw(false);
        console.log('Row updated in the DataTable:', updatedRow);
    } else {
        console.error('Row not found in the DataTable:', updatedRow);
    }
}




// Function to initialize DataTable
function LegislativeDataTable() {

    // Destroy existing DataTable if it exists
    if (legislative_dataTable) {
        legislative_dataTable.destroy();
   }

   // Get CSRF token
   const csrftoken = getCookie('csrftoken');
   legislative_dataTable = $('#legislative-table').DataTable({
       "dom": '<"top"Bf<"clear">><"top"lip<"clear">>rt<"bottom"<"clear">>',
       // autoWidth: false,
       scrollX: true,
       serverSide: true,
       orderCellsTop: true,
       rowReorder: true,
       ajax: {
           url: `/legislative/data_json/`,
           type: 'POST',
           dataType: 'json',
           headers: {
               'X-CSRFToken': csrftoken
           },
        },
       
       pageLength: 100,  // Set the number of records per page
       columns: [
            { data: 'id',  title: 'ID' },

            {
                data: 'member',
                title: 'Image',
                render: function (data, type, row) {
                    const imageUrl = `https://gov-finder.s3.amazonaws.com/images/${data.image_name}`;
                    return `<img style="width:80px;" src="${imageUrl}"/>`;
                }
            },

            { data: 'member',  title: 'Name',
                render: function (data, type, row){
                    if (data) {
                        return `<a style='white-space: nowrap;' href="${data.link}" target=_blank> ${data.name} </a>`;
                        } else {
                            return '';
                        }   
                }
            },

            { data: 'member',  title: 'State',
            render: function (data, type, row){
                return data ? data.state : '';
            }    
            },

            { data: 'member',  title: 'District',
            render: function (data, type, row){
                return data ? data.district : '';
            }    
            },

            { data: 'member',  title: 'Party',
            render: function (data, type, row){
                return data ? data.party : '';
            }    
            },

            { data: 'member',  title: 'Employer',
            render: function (data, type, row){
                return data ? data.employer : '';
            }    
        },
        
            { data: 'member',  title: 'Email',
            render: function (data, type, row){
                return data ? data.email : '';
            }    
            },


            { data: 'member',  title: 'Phone',
            render: function (data, type, row){
                return data ? data.phone : '';
            }    
            },


            { data: 'member',  title: 'Address',
            render: function (data, type, row){
                return data ? data.address : '';
            }    
            },

            { data: 'member',  title: 'Description',
            render: function (data, type, row){
                return data ? data.desc : '';
            }    
            },

            { data: 'member',  title: 'Member Title',
            render: function (data, type, row){
                return data ? data.member_title : '';
            }    
            },

            
            { data: 'title',  title: 'Committee Title',
            render: function (data, type, row){
                return data ? data.name : '';
            }    
            },
            

            { data: 'committee',  title: 'Committee',
                render: function (data, type, row){
                    if (data) {
                        return `<a href="${data.link}" target=_blank> ${data.name} </a>`;
                        } else {
                            return '';
                        }   
                }
            },

            { data: 'subcommittee',  title: 'Sub Committee',
                render: function (data, type, row){
                    if (data) {
                        return `<a href="${data.link}" target=_blank > ${data.name} </a>`;
                        } else {
                            return '';
                        }   
                }
            },

            { data: 'hierarchy',  title: 'Hierarchy',
            render: function (data, type, row){
                return data ? data.name : '';
            }    
            },

            { data: 'member',  title: 'image_name',
            render: function (data, type, row){
                return data ? data.image_name : '';
            }    
            },

            { data: 'subcommittee',  title: 'subcommittee_link',
            render: function (data, type, row){
                return data ? data.link : '';
            }    
            },

            { data: 'committee',  title: 'committee_link',
            render: function (data, type, row){
                return data ? data.link : '';
            }    
            },

            { data: 'member',  title: 'member_link',
            render: function (data, type, row){
                return data ? data.link : '';
            }    
            },

            { data: 'id', title: 'Delete',
            render: function (data, type, row){
                return `<button class="delete_data btn btn-danger" data-id="${data}">Delete</button>`;
            }    
            },
       ],

       // Include the searchHighlight extension
       searchHighlight: true,
       search: {
           regex: true,  // Disable regular expression search
           smart: false,  // Disable smart search
           caseInsensitive: true  // Make the search case-insensitive
       },
       buttons: [
           {
               extend: 'colvis',
               columns: ':not(.noVis)'
               
           },
           {
               extend: 'excel',
               text: 'Download File'
               // Add more buttons or options as needed
           }
       ],
       lengthMenu: [
           [ 100, 200, 500, 9999999 ],
           [ '100', '200', '500', 'All']
       ],
       
       // Additional DataTable options can be added here
       
       initComplete: function() {
        legislative_dataTable.draw();
       }

       
   });

       // Add the draw event listener for search highlighting
       legislative_dataTable.on('draw', function () {
        console.log('DataTable initialized.');
        var body = $(legislative_dataTable.table().body());
        body.unhighlight();
        body.highlight(legislative_dataTable.search());
    });
}

$(document).on('click', '.delete_data', function() {
    var id = $(this).data('id');
    $.ajax({
        url: `/legislative/delete_data/${id}`,
        type: 'POST',
        headers: {
            'X-CSRFToken': document.cookie.split('; ').find(c => c.startsWith('csrftoken')).split('=')[1],
        },
        success: function(response) {
            if(response.status === "success") {
                // Redraw the table
                legislative_dataTable.draw();
            } else {
                // Handle error
                console.error('Error deleting data');
            }
        },
        error: function(error) {
            // Handle error
            console.error('Error deleting data', error);
        }
    });
});






// Function to initialize DataTable
function CombineDataTable() {

    // Destroy existing DataTable if it exists
    if (combine_dataTable) {
        combine_dataTable.destroy();
   }

   // Get CSRF token
   const csrftoken = getCookie('csrftoken');
   combine_dataTable = $('#combine-table').DataTable({
       "dom": '<"container_datatable top"Bf<"clear">><"container_datatable top"lip<"clear">>rt<"bottom"<"clear">>',
       // autoWidth: false,
       scrollX: true,
       serverSide: true,
       orderCellsTop: true,
       rowReorder: true,
       ajax: {
           url: `/legislative/combine_data_json/`,
           type: 'POST',
           dataType: 'json',
           headers: {
               'X-CSRFToken': csrftoken
           },
        },
       
       pageLength: 100,  // Set the number of records per page
       columns: [
            { data: 'id',  title: 'ID' },

            {
                data: 'image_name',
                title: 'Image',
                render: function (data, type, row) {
                    const imageUrl = `https://gov-finder.s3.amazonaws.com/images/${data}`;
                    return `<img style="width:80px;" src="${imageUrl}"/>`;
                }
            },

            { data: 'name',  title: 'Name',
                render: function (data, type, row){
                    return data ? data : '';
                }
            },

            { data: 'state',  title: 'State',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            { data: 'district',  title: 'District',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            { data: 'party',  title: 'Party',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            { data: 'employer',  title: 'Employer',
            render: function (data, type, row){
                return data ? data : '';
            }    
        },
        
            { data: 'email',  title: 'Email',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },


            { data: 'phone_number',  title: 'Phone',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },


            { data: 'address',  title: 'Address',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            { data: 'desc',  title: 'Description',
            render: function (data, type, row){
                return data ? data : '';
            },
            width: '1000px' // Adjust the width as needed
            },

            { data: 'member_title',  title: 'Member Title',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            
            { data: 'committee_title',  title: 'Committee Title',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },
            

            { data: 'committee',  title: 'Committee',
                render: function (data, type, row){
                    return data ? data : '';
                }
            },

            { data: 'subcommittee',  title: 'Sub Committee',
                render: function (data, type, row){
                    return data ? data : ''; 
                }
            },

            { data: 'hierarchy',  title: 'Hierarchy',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            { data: 'image_name',  title: 'image_name',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            { data: 'subcommittee_link',  title: 'subcommittee_link',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            { data: 'committee_link',  title: 'committee_link',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            { data: 'member_link',  title: 'member_link',
            render: function (data, type, row){
                return data ? data : '';
            }    
            },

            // { data: 'id', title: 'Delete',
            // render: function (data, type, row){
            //     return `<button class="delete_data btn btn-danger" data-id="${data}">Delete</button>`;
            // }    
            // },
       ],

       // Include the searchHighlight extension
       searchHighlight: true,
       search: {
           regex: true,  // Disable regular expression search
           smart: false,  // Disable smart search
           caseInsensitive: true  // Make the search case-insensitive
       },
       buttons: [
           {
               extend: 'colvis',
               columns: ':not(.noVis)'
               
           },
           {
               extend: 'excel',
               text: 'Download File'
               // Add more buttons or options as needed
           }
       ],
       lengthMenu: [
           [ 100, 200, 500, 9999999 ],
           [ '100', '200', '500', 'All']
       ],
       
       // Additional DataTable options can be added here
       
       initComplete: function() {
        combine_dataTable.draw();
       }

       
   });

       // Add the draw event listener for search highlighting
       combine_dataTable.on('draw', function () {
        console.log('Combine DataTable initialized.');
        var body = $(combine_dataTable.table().body());
        body.unhighlight();
        body.highlight(combine_dataTable.search());
    });
}

$(document).on('click', '.delete_data', function() {
    var id = $(this).data('id');
    $.ajax({
        url: `/legislative/delete_data/${id}`,
        type: 'POST',
        headers: {
            'X-CSRFToken': document.cookie.split('; ').find(c => c.startsWith('csrftoken')).split('=')[1],
        },
        success: function(response) {
            if(response.status === "success") {
                // Redraw the table
                combine_dataTable.draw();
            } else {
                // Handle error
                console.error('Error deleting data');
            }
        },
        error: function(error) {
            // Handle error
            console.error('Error deleting data', error);
        }
    });
});