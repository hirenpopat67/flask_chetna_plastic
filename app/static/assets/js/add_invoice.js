var invoice_item_row_counter = 1
var fuse_customers;

// ADDING INVOICE ROWS ===================================================
function add_invoice_item_row() {
    old_item_row_count = invoice_item_row_counter
    invoice_item_row_counter++;
    
    $('#invoice-form-items-table-body >tr:last').clone(true).insertAfter('#invoice-form-items-table-body >tr:last');
    $('#invoice-form-items-table-body >tr:last input').val('');

    // $('#invoice-form-items-table-body >tr:last td')[1].innerHTML = invoice_item_row_counter
    // update_amounts($('#invoice-form-items-table-body input[name=invoice-qty]:last'));
}

function setup_invoice_rows() {
    $("#invoice-form-addrow").click(function(event) {
        event.preventDefault();
        add_invoice_item_row();
    });
    
    // for (var i = 0; i <= 3; i++) {
    //     add_invoice_item_row();
    // }
}


// JavaScript to toggle visibility

function toggleGSTRows() {
    var isChecked = document.getElementById("btn-check-outlined").checked;
    
    // Get the rows by their IDs
    var gstRow = document.getElementById("gst-row");
    var finalBillRow = document.getElementById("final-bill-row");
    
    // Toggle visibility based on checkbox state
    if (isChecked) {
        gstRow.style.display = '';
        finalBillRow.style.display = '';
    } else {
        gstRow.style.display = 'none';
        finalBillRow.style.display = 'none';
    }
}

// Call the function on page load to check initial checkbox state
document.addEventListener("DOMContentLoaded", function() {
    toggleGSTRows();
});


// function fetch_customer_details_by_name() {
//     var selectBox = document.getElementById('customer_name');

//     // Adding Event Listener for change event
//     selectBox.addEventListener('change', function () {
//         var selectedOption = selectBox.options[selectBox.selectedIndex];

//         // Get the customer name from the option value (only customer name, not place)
//         var customerName = selectedOption.value;

//         var customerPlace = selectedOption.getAttribute('data-place');
//         var customerMobile = selectedOption.getAttribute('data-mobile');
//         var customerGst = selectedOption.getAttribute('data-gst');
//         var discountPercentage = selectedOption.getAttribute('data-discount');

//         // Helper function to validate and set the value correctly
//         function setValidFieldValue(fieldId, value) {
//             var field = document.getElementById(fieldId);
//             // If the value is null, undefined, or "None", set it to an empty string
//             if (value === null || value === undefined || value === "None") {
//                 field.value = "";
//             } else {
//                 field.value = value;
//             }
//         }


//         // After selecting, update the select box to only display the customer name
//         selectBox.options[selectBox.selectedIndex].text = customerName;

//         // Set the respective fields using the helper function to avoid invalid values
//         setValidFieldValue("customer_place", customerPlace);
//         setValidFieldValue("customer_mobile_no", customerMobile);
//         setValidFieldValue("customer_gst_no", customerGst);
//         setValidFieldValue("discount_percentage", discountPercentage);
//     });
// }


// Fetching Product Details ===================================================

function fetch_product_details_by_name() {
    $('input[name="product_name"]').on('input', function() {
        var productName = $(this).val();
        var currentRow = $(this).closest('tr'); 
  
        if (productName.trim() !== "") {
              $.get(`/get_single_product/${productName}`,
                  function (data) {
                      // data = JSON.parse(data)
                      // console.log(data)
                     // Set the product_price input value in the same row from the API response
                    currentRow.find('input[name="product_price"]').val(data["product_price"]);
                  });
          } else {
              
                currentRow.find('input[name="product_price"]').val("");
          }})
}


// UPDATING INVOICE TOTALS ================================================

function update_invoice_totals() {
    // subtotal amount
    sub_total_amount = 0
    $('input[name=total_price_amount]').each(function () {
        // Use parseFloat with a fallback to 0 if the value is NaN
        sub_total_amount += parseFloat($(this).val()) || 0;
    });
    $('input[name=sub_total_amount]').val(sub_total_amount.toFixed(2));
    
    // Get the values
    var subTotal = parseFloat($("#sub_total_amount").val()) || 0;
    var discountPercentage = parseFloat($("#discount_percentage").val()) || 0;

    // Calculate discount amount
    var discountAmount = (discountPercentage / 100) * subTotal;

    // Update discount amount field
    $("#discount_amount").val(discountAmount.toFixed(2));

    // Calculate total amount
    var totalAmount = subTotal - discountAmount;

    // Update total amount field
    $("#total_amount").val(totalAmount.toFixed(2));

    // You can add more calculations for GST, final bill, etc., based on your requirements

    gst_amount = totalAmount * 18 / 100

    final_amount = totalAmount + gst_amount


    // For demonstration, let's set GST and final amount to 0
    $("#gst_amount").val(gst_amount.toFixed(2));
    $("#final_amount").val(final_amount.toFixed(2));
  }



// AUTO CALCULATE ITEM AMOUNTS =============================================

function initialize_auto_calculation(){
    update_amounts($('#invoice-form-items-table-body input[name=product_name]:first,input[name=qty]:first'));
    $('input[name=product_name],input[name=qty],input[name=product_price],input[name=total_price_amount],input[name=sub_total_amount],input[name=discount_percentage],input[name=discount_amount],input[name=total_amount],input[name=gst_amount],input[name=final_amount]').change(function (){
        update_amounts($(this));
    });
    update_amounts($('#invoice-form-items-table-body input[name=product_name]:first,input[name=qty]:first'));
    $('input[name=product_name],input[name=qty],input[name=product_price],input[name=total_price_amount],input[name=sub_total_amount],input[name=discount_percentage],input[name=discount_amount],input[name=total_amount],input[name=gst_amount],input[name=final_amount]').click(function (){
        update_amounts($(this));
    });
    update_amounts($('#invoice-form-items-table-body input[name=product_name]:first,input[name=qty]:first'));
    $('input[name=product_name],input[name=qty],input[name=product_price],input[name=total_price_amount],input[name=sub_total_amount],input[name=discount_percentage],input[name=discount_amount],input[name=total_amount],input[name=gst_amount],input[name=final_amount]').keyup(function (){
        update_amounts($(this));
    });
}

// Product Price Total ===================================================
function update_amounts(element){
    
    var product = parseInt(element.parent().parent().find('input[name=product_name]').val());
    var qty = parseInt(element.parent().parent().find('input[name=qty]').val());
    var product_price = parseInt(element.parent().parent().find('input[name=product_price]').val());

    var total_price_amount = qty * product_price 

    if(product == ""){
 
        total_price_amount = 0;
    }
    else {
    

    element.parent().parent().find('input[name=total_price_amount]').val(total_price_amount.toFixed(2));

    update_invoice_totals()

}}


function remove_product_row() {
    // Using event delegation on a parent element to handle dynamic content
    $(document).on('click', '.remove_row', function () {
        // Find the closest 'tr' element
        var $row = $(this).closest('tr');
        // Check if there is only one row in the table
        if ($row.siblings('tr').length === 0) {
            // If there is only one row, do nothing
            return;
        }
        // If there is more than one row, remove the current row
        $row.remove();
        initialize_auto_calculation()
    });
}

// START =============================================================

$(document).ready(function() {

    // Initialize invoice row addition
    setup_invoice_rows();

    // Initialize Fetch customer details
    // fetch_customer_details_by_name();
    
    
    // Initialize Fetch product details
    fetch_product_details_by_name();

    // Initialize product price total
    initialize_auto_calculation();

    // Initialize remove product row
    remove_product_row();
    
    // Initialize 
    convertToUpperCase();

})

function convertToUpperCase(input) {
    input.value = input.value.toUpperCase();
}
