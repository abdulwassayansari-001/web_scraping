let ec2_ip = '13.127.104.212:8000'
let placeholderImg = `http://${ec2_ip}/media/images/default.png`
let nullDataElement = null
let acceptedDataElement = null
let rejectedDataElement = null
let dataTable;

$(document).ready(function () {
    // Initially display the loader when the page loads
    document.getElementById('loader').style.display = 'none';
});

$(document).ready(function () {
    // Replace 'your-target-class' with the class you're checking for
    var null_data_class = document.querySelector('.null_data');
    var accepted_data_class = document.querySelector('.accepted_data');
    var rejected_data_class = document.querySelector('.rejected_data');

    // Check if the element with the target class exists on the page
    if (null_data_class) {
        // Your code to run when the class is present on this page
        console.log('Null Data');
        initDataTable('null');

        // Add your additional code here
    }
    if (accepted_data_class) {
        // Your code to run when the class is present on this page
        console.log('Accepted Data');
        initDataTable('true');

        // Add your additional code here
    }if (rejected_data_class) {
        // Your code to run when the class is present on this page
        console.log('Rejected Data');
        initDataTable('false');

        // Add your additional code here
    }
});

// Function to initialize DataTable
function initDataTable(validationStatus) {

     // Destroy existing DataTable if it exists
     if (dataTable) {
        dataTable.destroy();
    }

    dataTable = $('#leadership-table').DataTable({
        "dom": '<"top"f<"clear">><"top"lip<"clear">>rt<"bottom"ip<"clear">>',
        scrollX: true,
        serverSide: true,
        
        ajax: {
            url: `/get_data/?validation_status=${validationStatus}`, 
            type: 'GET',
            dataType: 'json',
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
            { data: 'hierarchy',  title: 'Hierarchy' },
            { data: 'validation',  title: 'Status' },
            {
                data: 'feedback_data',  title: 'Feedback',
                render: function (data, type, row) {
                    return `<textarea class="textarea" id="feedback_${row.id}">${data}</textarea>`;
                }
            },
            {
                data: 'id',  title: 'Accept',
                render: function (data, type, row) {
                    return `<button class="validate_accept submit_feedback btn btn-success" data-id="${data}">Accept</button>`;
                }
            },
            {
                data: 'id',  title: 'Reject',
                render: function (data, type, row) {
                    return `<button class="validate_reject submit_feedback btn btn-danger" data-id="${data}">Reject</button>`;
                }
            }
        ],

        // Include the searchHighlight extension
        searchHighlight: true,
        search: {
            smart: true,  // Enable smart search
            regex: true,  // Enable regular expression search
        },
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
            // Add more buttons as needed, see documentation for available options
        ],
        columnDefs: [
            {
                search: 'applied',
                regex: true,
                targets: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],  // Adjust column indices as needed
            },
            {
                targets: [9], 
                className: 'desc_class',
            },
            {
                targets: [10], 
                className: 'hierarchy_class',
            },
        ],
        lengthMenu: [
            [ 100, 200, 500, 1000 ],
            [ '100', '200', '500', '1000']
        ],
        // Additional DataTable options can be added here
    });

    // Add the draw event listener for search highlighting
    dataTable.on('draw', function () {
        console.log('DataTable initialized.');
        var body = $(dataTable.table().body());
        body.unhighlight();
        body.highlight(dataTable.search());
    });
}



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

function handleValidation(id, validation, feedbackText) {
    // Send a GET request to validate or reject the data
    const url = validation ? '/accepted_data/' : '/rejected_data/';
    $.ajax({
        url: url,
        method: 'GET',
        data: { id: id },
        dataType: 'json',
        success: function (response) {
            console.log('Data Validated:', response);

            // Update the DataTable row with the updated data
            updateDataTableRow(response.data);
            sendFeedback(id, feedbackText, function () {
                // Update the DataTable row after successfully submitting feedback
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
