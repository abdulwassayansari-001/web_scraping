let ec2_ip = '13.127.104.212:8000'
let placeholderImg = `http://${ec2_ip}/media/images/default.png`
let nullDataElement = null
let acceptedDataElement = null
let rejectedDataElement = null
let dataTable;

$(document).ready(function () {
    // Initially display the loader when the page loads
    document.getElementById('loader').style.display = 'none';

    // // Initialize DataTable when the page loads
    // initDataTable([]);

    // // Fetch initial data
    // fetchData();

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


// function fetchData() {
//     const length = 100; // Set your default items per page
//     const draw = 2; // Set the initial draw value

//     $.ajax({
//         url: `/get_data/?length=${length}&draw=${draw}`,
//         method: 'GET',
//         dataType: 'json',
//     })
//         .done(function (response) {
//             handleData(response);
//         })
//         .fail(function (jqXHR, textStatus, errorThrown) {
//             console.error('Error fetching data:', errorThrown);
//             // If there's an error, schedule another check after 1 second
//             setTimeout(fetchData, 1000);
//         });
// }

// function handleData(response) {
//     if ($.isPlainObject(response)) {
//         // If there is data, hide the loader and process the data
//         document.getElementById('loader').style.display = 'none';
//         // loadData(response);
//         // loadAcceptedData(response);
//         // loadRejectedData(response);
//     } else {
//         console.error('Invalid JSON data received:', response);
//     }
// }

// Function to initialize DataTable
function initDataTable(validationStatus) {

     // Destroy existing DataTable if it exists
     if (dataTable) {
        dataTable.destroy();
    }

    dataTable = $('#leadership-table').DataTable({
        serverSide: true,
        ajax: {
            url: `/get_data/?validation_status=${validationStatus}`, 
            type: 'GET',
            dataType: 'json',
        },
        pageLength: 10,  // Set the number of records per page
        columns: [
            { data: 'id' },
            { data: 'image_name', render: function (data, type, row) {
                const imageUrl = `https://gov-finder.s3.amazonaws.com/images/${data.replace(/\.(png|jpg|webp)$/, '')}.png`;
                return `<img style="width:100px;" src="${imageUrl}" onerror="this.src='${placeholderImg}'" />`;
            }},
            { data: 'name' },
            { data: 'designation' },
            { data: 'dep' },
            { data: 'address' },
            { data: 'email' },
            { data: 'phone_number' },
            {
                data: 'link',
                render: function (data, type, row) {
                    return `<a target="_blank" href="${data}">${data}</a>`;
                }
            },
            { data: 'desc' },
            { data: 'hierarchy' },
            { data: 'validation' },
            {
                data: 'feedback_data',
                render: function (data, type, row) {
                    return `<textarea class="textarea" id="feedback_${row.id}">${data}</textarea>`;
                }
            },
            {
                data: 'id',
                render: function (data, type, row) {
                    return `<button class="validate_accept submit_feedback btn btn-success" data-id="${data}">Accept</button>`;
                }
            },
            {
                data: 'id',
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
        columnDefs: [
            {
                search: 'applied',
                regex: true,
                targets: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],  // Adjust column indices as needed
            },
        ],

        // Additional DataTable options can be added here
    });

    // Add the draw event listener for search highlighting
    dataTable.on('draw', function () {
        var body = $(dataTable.table().body());
        body.unhighlight();
        body.highlight(dataTable.search());
    });
}



// $(document).ready(function () {
//     initDataTable('null');
// });

// function loadData(response) {
//     const scrapData = response.data;
//     console.log(scrapData)
//     // Sort the data by ID
//     scrapData.sort((a, b) => a.id - b.id);
//     console.log(scrapData)

//     const nullData = scrapData.filter(scrap_data => scrap_data.validation === null);
//     console.log("Unvalidated Data: " + nullData.length);

//     // Initialize DataTable
//     initDataTable(nullData);

//     // Add a click event listener to each "Accept" button
//     $(`#leadership_data [data-id].validate_accept`).click(function () {
//         const id = $(this).data('id');
//         acceptData(id);
//         const feedbackText = $(`#feedback_${id}`).val(); // Get the feedback text
//         console.log(feedbackText)
//         sendFeedback(id, feedbackText); // Send feedback data to the server
//     });

//     // Add a click event listener to each "Reject" button
//     $(`#leadership_data [data-id].validate_reject`).click(function () {
//         const id = $(this).data('id');
//         rejectData(id);
//         const feedbackText = $(`#feedback_${id}`).val(); // Get the feedback text
//         console.log(feedbackText)
//         sendFeedback(id, feedbackText); // Send feedback data to the server
//     });
// }


// function filter(response) {
//     const scrapData = response.scrap_data;
//     scrapData.sort((a, b) => a.id - b.id);

//     const uniqueHierarchies = new Set();
//     const hierarchyFilterDropdown = $('#hierarchyFilter'); // Create the dropdown dynamically
//     hierarchyFilterDropdown.empty().append('<option value="">All</option>'); // Add the "All" option as the default
//     const allData = scrapData.filter(scrap_data => scrap_data);

//     allData.forEach(function (s_data) {

//          // Check which separator is present in the hierarchy
//          let hierarchySeparator = " --> ";
//          if (s_data.hierarchy.includes("→")) {
//              hierarchySeparator = " → ";
//          }
//         const hierarchyParts = s_data.hierarchy.split(hierarchySeparator).slice(0, 3);
//         const filteredHierarchy = hierarchyParts.join(hierarchySeparator);

//         uniqueHierarchies.add(filteredHierarchy); // Use add() to add unique values to a Set
//     });

//        // Add distinct hierarchy values to the dropdown
//     uniqueHierarchies.forEach(function (filteredHierarchy) {
//         hierarchyFilterDropdown.append(`<option class="hierarchy_option" value="${filteredHierarchy}">${filteredHierarchy}</option>`);
//     });
// }

// function filterHierarchy() {
//     var input, filter, table, tr, td, i;
//     input = document.getElementById("hierarchyFilter");
//     filter = input.value;
//     table = document.querySelector(".leadership-data");
//     tr = table.getElementsByTagName("tr");
//     for (i = 0; i < tr.length; i++) {
//         td = tr[i].getElementsByTagName("td")[10];
//         if (td) {
//             var decodedHierarchy = td.innerHTML;
//             var temp = document.createElement("div");
//             temp.innerHTML = decodedHierarchy;
//             decodedHierarchy = temp.textContent || temp.innerText;
//             if (decodedHierarchy.indexOf(filter) > -1) {
//                     tr[i].style.display = "";
//             } else {
//                 tr[i].style.display = "none";
//             }
//         }
//     }
// }

function sendFeedback(id, feedbackText) {
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
        } else {
            console.log('Error: ' + data.errors);
        }
    })
    .catch(error => console.error('Error:', error));
}

// function loadAcceptedData(response) {
//     const scrapData = response.scrap_data;
//     // Sort the data by ID
//     scrapData.sort((a, b) => a.id - b.id);
//     const loadDataAcceptedTable = $('#leadership_data_accepted');
    
//     loadDataAcceptedTable.empty();

    
//     const acceptedData = scrapData.filter(scrap_data => scrap_data.validation);              
//     console.log("Accepted Data:" + acceptedData.length)

//     acceptedData.forEach(function (s_data) {

//         // Remove both ".png", "webp" and ".jpg" extensions from s_data.image_name
//         const image_name = s_data.image_name.replace(/\.(png|jpg|webp)$/, '');

//         // // Construct the image URL
//         const imageUrl = `https://gov-finder.s3.amazonaws.com/images/${image_name}.png`;

//         const validationText = s_data.validation ? 'Accepted' : 'Rejected';
//         const row = `<tr>
//             <td>${s_data.id}</td>
//             <td class="images" >
//                 <img src="${imageUrl}" onerror="this.src='${placeholderImg}'" />
//             </td>
//             <td>${s_data.name}</td>
//             <td>${s_data.designation}</td>
//             <td>${s_data.dep}</td>
//             <td>${s_data.address}</td>
//             <td>${s_data.email}</td>
//             <td>${s_data.phone_number}</td>
//             <td><a target=_blank href="${s_data.link}">${s_data.link}</a></td>
//             <td>${s_data.desc}</td>
//             <td>${s_data.hierarchy}</td>
//             <td>${s_data.feedback_data}</td>
//             <td>${validationText}</td>
//             <td>
//                 <button class="validate_reject btn btn-danger" data-id="${s_data.id}">Reject</button>
//             </td>
//         </tr>`;
//         loadDataAcceptedTable.append(row);
//     });

//         // Show or hide the table based on whether there is data
//         if (acceptedData.length > 0) {
//         $('#leadership_table_accepted').show();
//     } else {
//         $('#leadership_table_accepted').hide();
//     }
//     }

// function loadRejectedData(response) {
//     const scrapData = response.scrap_data;
//     // Sort the data by ID
//     scrapData.sort((a, b) => a.id - b.id);
//     const loadDataRejectedTable = $('#leadership_data_rejected');

//     loadDataRejectedTable.empty();

//     const rejectedData = scrapData.filter(scrap_data => scrap_data.validation === false);
//     console.log("Rejected Data:" + rejectedData.length)
    
//     rejectedData.forEach(function (s_data) {

//         // Remove both ".png", "webp" and ".jpg" extensions from s_data.image_name
//         const image_name = s_data.image_name.replace(/\.(png|jpg|webp)$/, '');

//         // // Construct the image URL
//         const imageUrl = `https://gov-finder.s3.amazonaws.com/images/${image_name}.png`;
        
//         const validationText = s_data.validation ? 'Accepted' : 'Rejected';
//         const row = `<tr>
//             <td>${s_data.id}</td>
//             <td class="images" >
//                 <img src="${imageUrl}" onerror="this.src='${placeholderImg}'" />
//             </td>
//             <td>${s_data.name}</td>
//             <td>${s_data.designation}</td>
//             <td>${s_data.dep}</td>
//             <td>${s_data.address}</td>
//             <td>${s_data.email}</td>
//             <td>${s_data.phone_number}</td>
//             <td><a target=_blank href="${s_data.link}">${s_data.link}</a></td>
//             <td>${s_data.desc}</td>
//             <td>${s_data.hierarchy}</td>
//             <td>${s_data.feedback_data}</td>
//             <td>${validationText}</td>
//             <td>
//                 <button class="validate_accept btn btn-success" data-id="${s_data.id}">Accept</button>
//             </td>
//         </tr>`;
//         loadDataRejectedTable.append(row);
//     });

//     // Show or hide the table based on whether there is data
//     if (rejectedData.length > 0) {
//         $('#leadership_table_rejected').show();
//     } else {
//         $('#leadership_table_rejected').hide();
//     }
// }

// Use event delegation for dynamically added elements
$(document).on('click', '.validate_accept', function () {
    const id = $(this).data('id');
    handleValidation(id, true);
});

$(document).on('click', '.validate_reject', function () {
    const id = $(this).data('id');
    handleValidation(id, false);
});

function handleValidation(id, validation) {
    // Send a GET request to validate or reject the data
    const url = validation ? '/accepted_data/' : '/rejected_data/';
    $.ajax({
        url: url,
        method: 'GET',
        data: { id: id },
        dataType: 'json',
        success: function (response) {
            console.log('Data Validated:', response);
            initDataTable('null'); // Update the data after validation
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('Error Validating Data:', errorThrown);
        },
    });
}
