// Initially display the loader when the page loads
$(document).ready(function(){
    document.getElementById('loader').style.display = 'block';
});

// Call the fetchData function
fetchData();

function fetchData() {
    $.ajax({
        url: '/get_data/',
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            if ($.isPlainObject(response)) {
                // If there is data, hide the loader and process the data
                document.getElementById('loader').style.display = 'none';
                loadData(response, '#leadership_data');
                loadAcceptedData(response, '#leadership_data_accepted');
                loadRejectedData(response, '#leadership_data_rejected');
                filter(response)
                // filterHierarchy(response)
            } else {
                console.error('Invalid JSON data received:', response);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('Error fetching data:', errorThrown);
            // If there's an error, schedule another check after 3 seconds
            setTimeout(fetchData, 1000);
        }
    });
}

fetchData()
// setTimeout(fetchData, 3000)

function filter(response) {
    const scrapData = response.scrap_data;
    scrapData.sort((a, b) => a.id - b.id);

    const uniqueHierarchies = new Set();
    const hierarchyFilterDropdown = $('#hierarchyFilter'); // Create the dropdown dynamically
    hierarchyFilterDropdown.empty().append('<option value="">All</option>'); // Add the "All" option as the default
    const allData = scrapData.filter(scrap_data => scrap_data);

    allData.forEach(function (s_data) {

         // Check which separator is present in the hierarchy
         let hierarchySeparator = " --> ";
         if (s_data.hierarchy.includes("→")) {
             hierarchySeparator = " → ";
         }
        const hierarchyParts = s_data.hierarchy.split(hierarchySeparator).slice(0, 3);
        const filteredHierarchy = hierarchyParts.join(hierarchySeparator);

        uniqueHierarchies.add(filteredHierarchy); // Use add() to add unique values to a Set
    });

       // Add distinct hierarchy values to the dropdown
    uniqueHierarchies.forEach(function (filteredHierarchy) {
        hierarchyFilterDropdown.append(`<option class="hierarchy_option" value="${filteredHierarchy}">${filteredHierarchy}</option>`);
    });
}

function filterHierarchy() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("hierarchyFilter");
    filter = input.value;
    table = document.querySelector(".leadership-data");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[10];
        if (td) {
            var decodedHierarchy = td.innerHTML;
            var temp = document.createElement("div");
            temp.innerHTML = decodedHierarchy;
            decodedHierarchy = temp.textContent || temp.innerText;
            if (decodedHierarchy.indexOf(filter) > -1) {
                    tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function loadData(response) {
    const scrapData = response.scrap_data;
    // Sort the data by ID
    scrapData.sort((a, b) => a.id - b.id);
    const loadDataTable = $('#leadership_data');

    loadDataTable.empty();

    const nullData = scrapData.filter(scrap_data => scrap_data.validation === null);
    nullData.forEach(function (s_data) {

        // // Construct the image URL
        const imageUrl = `http://localhost:9000/images/${s_data.image_name}`;

        ec2_ip = '13.127.104.212:8000'

        const placeholderImg = `http://${ec2_ip}/media/images/default.png`

        // Create an image element
        const imageElement = document.createElement('img');
        imageElement.src = placeholderImg;
        imageElement.alt = `${s_data.name}'s Image`;
        imageElement.width = 100;
        imageElement.height = 100;
        imageElement.className = 'images';


        // Add an error event listener to replace the image with a placeholder if it fails to load
        imageElement.addEventListener('error', function () {
            imageElement.src = placeholderImg;
        });
        
        const row = `<tr>
            <td>${s_data.id}</td>
            <td>
                ${imageElement.outerHTML}
            </td>
            <td>${s_data.name}</td>
            <td>${s_data.designation}</td>
            <td>${s_data.dep}</td>
            <td>${s_data.address}</td>
            <td>${s_data.email}</td>
            <td>${s_data.phone_number}</td>
            <td><a target="_blank" href="${s_data.link}">${s_data.link}</a></td>
            <td class='description' >${s_data.desc}</td>
            <td>${s_data.hierarchy}</td>
            <td class="validate_button">
                <button class="validate_accept btn btn-success" data-id="${s_data.id}">Accept</button>
            </td>
            <td class="validate_button">
                <button class="validate_reject btn btn-danger" data-id="${s_data.id}">Reject</button>
            </td>
        </tr>`;
        loadDataTable.append(row);
    });

    // Add a click event listener to each row
    $('.validate_accept').click(function () {
        const id = $(this).data('id');
        acceptData(id);
    });

    // Add a click event listener to each row
    $('.validate_reject').click(function () {
        const id = $(this).data('id');
        rejectData(id);
    });
}

function loadAcceptedData(response) {
    const scrapData = response.scrap_data;
    // Sort the data by ID
    scrapData.sort((a, b) => a.id - b.id);
    const loadDataAcceptedTable = $('#leadership_data_accepted');
    
    loadDataAcceptedTable.empty();

    
    const acceptedData = scrapData.filter(scrap_data => scrap_data.validation);              
    acceptedData.forEach(function (s_data) {
        const imageUrl = `http://localhost:9000/images/${s_data.image_name}`;
        const validationText = s_data.validation ? 'Accepted' : 'Rejected';
        const row = `<tr>
            <td>${s_data.id}</td>
            <td>
                <img src="${imageUrl}" alt="${s_data.name}">
            </td>
            <td>${s_data.name}</td>
            <td>${s_data.designation}</td>
            <td>${s_data.dep}</td>
            <td>${s_data.address}</td>
            <td>${s_data.email}</td>
            <td>${s_data.phone_number}</td>
            <td><a target=_blank href="${s_data.link}">${s_data.link}</a></td>
            <td>${s_data.desc}</td>
            <td>${s_data.hierarchy}</td>
            <td>${validationText}</td>
            <td>
                <button class="validate_reject btn btn-danger" data-id="${s_data.id}">Reject</button>
            </td>
        </tr>`;
        loadDataAcceptedTable.append(row);
    });

        // Show or hide the table based on whether there is data
        if (acceptedData.length > 0) {
        $('#leadership_table_accepted').show();
    } else {
        $('#leadership_table_accepted').hide();
    }

            // Add a click event listener to each row
            $('.validate_reject').click(function () {
            const id = $(this).data('id');
            rejectData(id);
        });
    }

function loadRejectedData(response) {
    const scrapData = response.scrap_data;
    // Sort the data by ID
    scrapData.sort((a, b) => a.id - b.id);
    const loadDataRejectedTable = $('#leadership_data_rejected');

    loadDataRejectedTable.empty();

    const acceptedData = scrapData.filter(scrap_data => scrap_data.validation === false);
    acceptedData.forEach(function (s_data) {
        const imageUrl = `http://localhost:9000/images/${s_data.image_name}`;
        const validationText = s_data.validation ? 'Accepted' : 'Rejected';
        const row = `<tr>
            <td>${s_data.id}</td>
            <td>
                <img src="${imageUrl}" alt="${s_data.name}">
            </td>
            <td>${s_data.name}</td>
            <td>${s_data.designation}</td>
            <td>${s_data.dep}</td>
            <td>${s_data.address}</td>
            <td>${s_data.email}</td>
            <td>${s_data.phone_number}</td>
            <td><a target=_blank href="${s_data.link}">${s_data.link}</a></td>
            <td>${s_data.desc}</td>
            <td>${s_data.hierarchy}</td>
            <td>${validationText}</td>
            <td>
                <button class="validate_accept btn btn-success" data-id="${s_data.id}">Accept</button>
            </td>
        </tr>`;
        loadDataRejectedTable.append(row);
    });

    // Show or hide the table based on whether there is data
    if (acceptedData.length > 0) {
        $('#leadership_table_rejected').show();
    } else {
        $('#leadership_table_rejected').hide();
    }

    // Add a click event listener to each row
    $('.validate_accept').click(function () {
        const id = $(this).data('id');
        acceptData(id);
    });
}

function acceptData(id) {
    // Send a GET request to Validate the data
    $.ajax({
        url: '/accepted_data/',
        method: 'GET',
        data: { id: id },
        dataType: 'json',
        success: function (response) {
            console.log('Data Validated:', response);
            fetchData()
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('Error Validating Data:', errorThrown);
        }
    });
}

function rejectData(id) {
    // Send a GET request to Validate the data
    $.ajax({
        url: '/rejected_data/',
        method: 'GET',
        data: { id: id },
        dataType: 'json',
        success: function (response) {
            console.log('Data Validated:', response);
            fetchData()
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('Error Validating Data:', errorThrown);
        }
    });
}
