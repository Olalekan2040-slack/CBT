// Main JavaScript for CBT System

$(document).ready(function() {
    // Initialize animations
    initializeAnimations();
    
    // Initialize exam timer if on exam page
    if ($('#exam-timer').length) {
        initializeExamTimer();
    }
    
    // Initialize auto-save for exam answers
    if ($('.exam-form').length) {
        initializeAutoSave();
    }
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize form validations
    initializeFormValidations();
});

// Animation Initialization
function initializeAnimations() {
    // Fade in cards on scroll
    $(window).scroll(function() {
        $('.card, .dashboard-card, .exam-card').each(function() {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            
            if (elementBottom > viewportTop && elementTop < viewportBottom) {
                $(this).addClass('animate__animated animate__fadeInUp');
            }
        });
    });
    
    // Hover effects for buttons
    $('.btn').hover(
        function() {
            $(this).addClass('animate__animated animate__pulse');
        },
        function() {
            $(this).removeClass('animate__animated animate__pulse');
        }
    );
}

// Exam Timer Functionality
function initializeExamTimer() {
    var remainingTime = parseInt($('#exam-timer').data('remaining-time'));
    var warningTime = 300; // 5 minutes
    
    var timer = setInterval(function() {
        remainingTime--;
        
        var hours = Math.floor(remainingTime / 3600);
        var minutes = Math.floor((remainingTime % 3600) / 60);
        var seconds = remainingTime % 60;
        
        var display = pad(hours) + ':' + pad(minutes) + ':' + pad(seconds);
        $('#exam-timer').text(display);
        
        // Warning when time is running low
        if (remainingTime <= warningTime) {
            $('#exam-timer').addClass('timer-warning');
            
            // Show warning message
            if (remainingTime === warningTime) {
                showNotification('warning', 'Only 5 minutes remaining!');
            }
        }
        
        // Auto-submit when time is up
        if (remainingTime <= 0) {
            clearInterval(timer);
            $('#exam-timer').text('00:00:00');
            showNotification('danger', 'Time is up! Submitting exam...');
            submitExam(true); // Auto-submit
        }
    }, 1000);
    
    // Store timer reference for cleanup
    window.examTimer = timer;
}

// Auto-save Functionality
function initializeAutoSave() {
    var autoSaveInterval = setInterval(function() {
        autoSaveAnswers();
    }, 30000); // Auto-save every 30 seconds
    
    // Save on answer change
    $('.exam-form input[type="radio"]').change(function() {
        autoSaveAnswers();
        updateProgress();
    });
    
    // Store interval reference for cleanup
    window.autoSaveInterval = autoSaveInterval;
}

// Auto-save answers
function autoSaveAnswers() {
    var answers = {};
    $('.exam-form input[type="radio"]:checked').each(function() {
        var questionId = $(this).attr('name').replace('question_', '');
        answers[questionId] = $(this).val();
    });
    
    // Store in localStorage as backup
    localStorage.setItem('exam_answers', JSON.stringify(answers));
    
    // Visual feedback
    $('#auto-save-indicator').fadeIn().delay(1000).fadeOut();
}

// Update progress bar
function updateProgress() {
    var totalQuestions = $('.question-card').length;
    var answeredQuestions = $('.exam-form input[type="radio"]:checked').length;
    var percentage = (answeredQuestions / totalQuestions) * 100;
    
    $('#progress-bar').css('width', percentage + '%');
    $('#progress-text').text(answeredQuestions + ' of ' + totalQuestions + ' questions answered');
}

// Submit exam
function submitExam(autoSubmit = false) {
    if (!autoSubmit) {
        if (!confirm('Are you sure you want to submit your exam? This action cannot be undone.')) {
            return;
        }
    }
    
    // Disable submit button
    $('#submit-btn').prop('disabled', true).html('<span class="loading-spinner"></span> Submitting...');
    
    // Collect answers
    var answers = {};
    $('.exam-form input[type="radio"]:checked').each(function() {
        var questionId = $(this).attr('name').replace('question_', '');
        answers[questionId] = $(this).val();
    });
    
    // Get CSRF token
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    
    // Submit via AJAX
    $.ajax({
        url: $('#exam-form').data('submit-url'),
        method: 'POST',
        data: JSON.stringify({
            answers: answers,
            csrfmiddlewaretoken: csrfToken
        }),
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(response) {
            if (response.success) {
                // Clear localStorage
                localStorage.removeItem('exam_answers');
                
                // Clear timers
                if (window.examTimer) clearInterval(window.examTimer);
                if (window.autoSaveInterval) clearInterval(window.autoSaveInterval);
                
                // Redirect to results
                showNotification('success', 'Exam submitted successfully!');
                setTimeout(function() {
                    window.location.href = response.redirect_url;
                }, 1500);
            } else {
                showNotification('danger', 'Error submitting exam. Please try again.');
                $('#submit-btn').prop('disabled', false).html('Submit Exam');
            }
        },
        error: function() {
            showNotification('danger', 'Network error. Please check your connection and try again.');
            $('#submit-btn').prop('disabled', false).html('Submit Exam');
        }
    });
}

// Smooth scrolling
function initializeSmoothScrolling() {
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });
}

// Form validations
function initializeFormValidations() {
    // Real-time validation
    $('.form-control').on('blur', function() {
        validateField($(this));
    });
    
    // Form submission validation
    $('form').on('submit', function(e) {
        var isValid = true;
        $(this).find('.form-control').each(function() {
            if (!validateField($(this))) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showNotification('danger', 'Please fix the errors in the form.');
        }
    });
}

// Field validation
function validateField(field) {
    var value = field.val().trim();
    var isValid = true;
    var errorMessage = '';
    
    // Required field validation
    if (field.prop('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required.';
    }
    
    // Email validation
    if (field.attr('type') === 'email' && value) {
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address.';
        }
    }
    
    // Password validation
    if (field.attr('name') === 'password1' && value) {
        if (value.length < 8) {
            isValid = false;
            errorMessage = 'Password must be at least 8 characters long.';
        }
    }
    
    // Password confirmation
    if (field.attr('name') === 'password2' && value) {
        var password1 = $('input[name="password1"]').val();
        if (value !== password1) {
            isValid = false;
            errorMessage = 'Passwords do not match.';
        }
    }
    
    // Update field styling
    if (isValid) {
        field.removeClass('is-invalid').addClass('is-valid');
        field.siblings('.invalid-feedback').remove();
    } else {
        field.removeClass('is-valid').addClass('is-invalid');
        field.siblings('.invalid-feedback').remove();
        field.after('<div class="invalid-feedback">' + errorMessage + '</div>');
    }
    
    return isValid;
}

// Notification system
function showNotification(type, message) {
    var alertClass = 'alert-' + type;
    var notification = `
        <div class="alert ${alertClass} alert-dismissible fade show animate__animated animate__fadeInDown" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Remove existing notifications
    $('.alert').remove();
    
    // Add new notification
    $('main').prepend('<div class="container mt-3">' + notification + '</div>');
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
}

// Utility function to pad numbers
function pad(num) {
    return num < 10 ? '0' + num : num;
}

// Page-specific functions
$(document).ready(function() {
    // Dashboard animations
    if ($('.dashboard-card').length) {
        $('.dashboard-card').each(function(index) {
            $(this).delay(index * 200).queue(function() {
                $(this).addClass('animate__animated animate__fadeInUp').dequeue();
            });
        });
    }
    
    // Exam list animations
    if ($('.exam-card').length) {
        $('.exam-card').each(function(index) {
            $(this).delay(index * 150).queue(function() {
                $(this).addClass('animate__animated animate__fadeInLeft').dequeue();
            });
        });
    }
    
    // Results page animations
    if ($('.result-card').length) {
        $('.result-card').addClass('animate__animated animate__fadeInUp');
    }
});

// Handle exam start
function startExam(examId) {
    if (confirm('Are you ready to start the exam? Once started, the timer will begin.')) {
        window.location.href = '/exams/start/' + examId + '/';
    }
}

// Handle navigation warning during exam
window.addEventListener('beforeunload', function(e) {
    if ($('#exam-timer').length && window.examTimer) {
        e.preventDefault();
        e.returnValue = 'You are currently taking an exam. Are you sure you want to leave?';
        return e.returnValue;
    }
});

// Restore answers from localStorage on page load
$(document).ready(function() {
    if ($('.exam-form').length) {
        var savedAnswers = localStorage.getItem('exam_answers');
        if (savedAnswers) {
            try {
                var answers = JSON.parse(savedAnswers);
                for (var questionId in answers) {
                    $('input[name="question_' + questionId + '"][value="' + answers[questionId] + '"]').prop('checked', true);
                }
                updateProgress();
            } catch (e) {
                console.log('Error restoring answers:', e);
            }
        }
    }
});

// Mobile-specific optimizations
if (window.innerWidth <= 768) {
    // Reduce animation duration for mobile
    $('.animate__animated').css('animation-duration', '0.5s');
    
    // Optimize touch interactions
    $('.card, .btn').on('touchstart', function() {
        $(this).addClass('touched');
    }).on('touchend', function() {
        setTimeout(() => {
            $(this).removeClass('touched');
        }, 150);
    });
}
