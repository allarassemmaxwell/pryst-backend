

$(document).ready(function() {
    
    // $("#vertical-menu-btn").click(function() {
    //     $('#vertical-menu').toggle('slow'); 
    // });

    // CLOSE ALERT IN LOGIN PAGE
    $('.close').click(function() {
        $('.alert').toggle('slow'); 
    });

    // $('#outlet').click(function() {
    //     $('#hideOutlet').toggle('slow'); 
    // });

    // $('#county').click(function() {
    //     $('#hideCounty').toggle('slow'); 
    // });
    // $('#product').click(function() {
    //     $('#hideProduct').toggle('slow'); 
    // });

    $(".audit-edit-form").validate({
        rules: {  
            outlet_slug: 'required',
            product_slug: 'required',
            user: 'required',
            price: {
				required: true,
				number: true
			},
            measure: 'required', 
        },
        messages: {
            outlet_slug: {
                required: "This field is required."
            },                        
            product_slug: {
                required: "This field is required."
            },
            user: {
                required: "This field is required."
            }
        }
    });

    // ADD BRAND FORM VALIDATION
    $(".brand-add-form").validate({
        rules: { name: 'required' }
    });

    // EDIT BRAND FORM VALIDATION
    $(".brand-edit-form").validate({
        rules: {  name: 'required' }
    });

    // ADD MODEL FORM VALIDATION
    $(".model-add-form").validate({
        rules: {  
            name: 'required', 
            brand_slug: 'required' 
        },
        messages: {
            brand_slug: {
                required: "This field is required."
            }
        }
    });

    // EDIT MODEL FORM VALIDATION
    $(".model-edit-form").validate({
        rules: {  
            name: 'required', 
            brand_slug: 'required' 
        },
        messages: {
            brand_slug: {
                required: "This field is required."
            }
        }
    });



    // ADD COUNTY FORM VALIDATION
    $(".county-add-form").validate({
        rules: { name: 'required'}
    });

    // EDIT COUNTY FORM VALIDATION
    $(".county-edit-form").validate({
        rules: { name: 'required'}
    });




    // ADD OUTLET FORM VALIDATION
    $(".outlet-add-form").validate({
        rules: {  
            name: 'required', 
            user_email: 'required',
            category_slug: 'required' 
        },
        messages: {
            user_email: {
                required: "This field is required."
            },
            category_slug: {
                required: "This field is required."
            }
        }
    });

    // EDIT OUTLET FORM VALIDATION
    $(".outlet-edit-form").validate({
        rules: {  
            name: 'required', 
            user_email: 'required',
            category_slug: 'required' 
        },
        messages: {
            user_email: {
                required: "This field is required."
            },
            category_slug: {
                required: "This field is required."
            }
        }
    });


    // ADD OUTLET CATEGORY FORM VALIDATION
    $(".outlet-category-add-form").validate({
        rules: { name: 'required'}
    });

    // EDIT OUTLET CATEGORY FORM VALIDATION
    $(".outlet-category-edit-form").validate({
        rules: { name: 'required'}
    });



    // ADD PRODUCT FORM VALIDATION
    $(".product-add-form").validate({
        rules: {  
            name: 'required', 
            model_slug: 'required',
            measure: 'required',
            category_slug: 'required',
            manufacturer: 'required' 
        },
        messages: {
            model_slug: {
                required: "This field is required."
            },                        
            category_slug: {
                required: "This field is required."
            }
        }
    });

    // EDIT PRODUCT FORM VALIDATION
    $(".product-edit-form").validate({
        rules: {  
            name: 'required', 
            model_slug: 'required',
            measure: 'required',
            category_slug: 'required',
            manufacturer: 'required' 
        },
        messages: {
            model_slug: {
                required: "This field is required."
            },                        
            category_slug: {
                required: "This field is required."
            }
        }
    });

    // ADD PRODUCT CATEGORY FORM VALIDATION
    $(".product-category-add-form").validate({
        rules: { name: 'required'}
    });

    // EDIT OUTLET CATEGORY FORM VALIDATION
    $(".product-category-edit-form").validate({
        rules: { name: 'required'}
    });



    // ADD USER FORM VALIDATION
    $(".user-add-form").validate({
        rules: {  
            first_name: 'required',
            last_name: 'required', 
            email: {
                required: true,
                email: true
            },
            county_slug: 'required',
            admin: 'required',
            active: 'required',
            password1: {
                required: true,
                minlength: 6
            },
            password2: {
                required: true,
                equalTo : "#password1"
            } 
        },
        messages: {
            county_slug: {
                required: "This field is required."
            },                        
            admin: {
                required: "This field is required."
            },
            active: {
                required: "This field is required."
            }
        }
    });



    // EDIT USER FORM VALIDATION
    $(".user-edit-form").validate({
        rules: {  
            first_name: 'required',
            last_name: 'required', 
            email: {
                required: true,
                email: true
            },
            county_slug: 'required',
            admin: 'required',
            active: 'required'
        },
        messages: {
            county_slug: {
                required: "This field is required."
            },                        
            admin: {
                required: "This field is required."
            },
            active: {
                required: "This field is required."
            }
        }
    });



    // CHANGE USER PASSWORD FOR VALIDATION
    $(".change-user-password-form").validate({
        rules: {  
            password1: {
                required: true,
                minlength: 6
            },
            password2: {
                required: true,
                equalTo : "#password1"
            } 
        }
    });



    // LOGIN FORM VALIDATION
    $(".login-form").validate({
        rules: {
            username: {
                required: true,
                email: true
            },
            password: 'required'
        }
    });


    // RESET USER PASSWORD FORM VALIDATION
    $(".reset-user-password-form").validate({
        rules: {
            email: {
                required: true,
                email: true
            }
        }
    });




});

