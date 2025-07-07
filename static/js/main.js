// Main JavaScript file for SocialSphere

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Like functionality
    $('.like-btn').click(function(e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        var btn = $(this);
        
        $.ajax({
            url: '/post/' + postId + '/like/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                var icon = btn.find('i');
                var count = btn.find('.likes-count');
                
                if (data.liked) {
                    icon.removeClass('far').addClass('fas text-danger');
                } else {
                    icon.removeClass('fas text-danger').addClass('far');
                }
                
                count.text(data.likes_count);
            },
            error: function() {
                alert('An error occurred. Please try again.');
            }
        });
    });

    // Comment form submission
    $('.comment-form').submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var postId = form.data('post-id');
        var submitBtn = form.find('button[type="submit"]');
        var originalText = submitBtn.text();
        
        submitBtn.prop('disabled', true).html('<span class="loading"></span> Posting...');
        
        $.ajax({
            url: '/post/' + postId + '/comment/',
            type: 'POST',
            data: form.serialize(),
            success: function(data) {
                // Reload the page to show the new comment
                location.reload();
            },
            error: function() {
                alert('An error occurred. Please try again.');
                submitBtn.prop('disabled', false).text(originalText);
            }
        });
    });

    // Check for new notifications
    function checkNotifications() {
        $.ajax({
            url: '/notifications/',
            type: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(data) {
                var badge = $('#notification-badge');
                if (data.unread_count > 0) {
                    badge.text(data.unread_count).show();
                } else {
                    badge.hide();
                }
            }
        });
    }

    // Check notifications every 30 seconds
    setInterval(checkNotifications, 30000);

    // File input preview
    $('input[type="file"]').change(function() {
        var input = $(this);
        var file = input[0].files[0];
        var preview = input.siblings('.file-preview');
        
        if (file && file.type.startsWith('image/')) {
            var reader = new FileReader();
            reader.onload = function(e) {
                if (preview.length === 0) {
                    preview = $('<div class="file-preview mt-2"></div>');
                    input.after(preview);
                }
                preview.html('<img src="' + e.target.result + '" class="img-fluid rounded" style="max-height: 200px;">');
            };
            reader.readAsDataURL(file);
        } else if (preview.length > 0) {
            preview.remove();
        }
    });

    // Search functionality
    var searchTimeout;
    $('input[name="q"]').on('input', function() {
        clearTimeout(searchTimeout);
        var query = $(this).val();
        
        if (query.length > 2) {
            searchTimeout = setTimeout(function() {
                // You can implement live search here
                // For now, we'll just submit the form when user presses Enter
            }, 500);
        }
    });

    // Infinite scroll for posts (optional enhancement)
    var loading = false;
    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
            if (!loading) {
                loading = true;
                var nextPage = $('.pagination .page-item.active .page-link').text();
                var hasNext = $('.pagination .page-item:last-child .page-link').text() === 'Next';
                
                if (hasNext) {
                    loadMorePosts(parseInt(nextPage) + 1);
                }
            }
        }
    });

    function loadMorePosts(page) {
        var currentUrl = window.location.pathname + window.location.search;
        var separator = currentUrl.includes('?') ? '&' : '?';
        var url = currentUrl + separator + 'page=' + page;
        
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                // Parse the response and append new posts
                // This would require server-side changes to return JSON
                loading = false;
            },
            error: function() {
                loading = false;
            }
        });
    }

    // Share functionality
    $('.share-btn').click(function(e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        window.open('/post/' + postId + '/share/', 'Share Post', 'width=500,height=400');
    });

    // Follow/Unfollow functionality
    $('.follow-btn').click(function(e) {
        e.preventDefault();
        var username = $(this).data('username');
        var btn = $(this);
        var originalText = btn.text();
        
        btn.prop('disabled', true).html('<span class="loading"></span>');
        
        $.ajax({
            url: '/profiles/user/' + username + '/follow/',
            type: 'GET',
            success: function(data) {
                // Reload the page to update the button state
                location.reload();
            },
            error: function() {
                alert('An error occurred. Please try again.');
                btn.prop('disabled', false).text(originalText);
            }
        });
    });

    // Profile picture upload preview
    $('#id_profile_picture').change(function() {
        var file = this.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('.profile-picture-preview').attr('src', e.target.result);
            };
            reader.readAsDataURL(file);
        }
    });

    // Cover photo upload preview
    $('#id_cover_photo').change(function() {
        var file = this.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('.cover-photo-preview').attr('src', e.target.result);
            };
            reader.readAsDataURL(file);
        }
    });

    // Post form character counter
    $('#id_content').on('input', function() {
        var maxLength = 1000; // Set your desired max length
        var currentLength = $(this).val().length;
        var counter = $(this).siblings('.char-counter');
        
        if (counter.length === 0) {
            counter = $('<small class="char-counter text-muted"></small>');
            $(this).after(counter);
        }
        
        counter.text(currentLength + '/' + maxLength);
        
        if (currentLength > maxLength * 0.9) {
            counter.addClass('text-warning');
        } else {
            counter.removeClass('text-warning');
        }
        
        if (currentLength > maxLength) {
            counter.addClass('text-danger');
        } else {
            counter.removeClass('text-danger');
        }
    });

    // Mobile menu toggle
    $('.navbar-toggler').click(function() {
        $('.navbar-collapse').toggleClass('show');
    });

    // Close mobile menu when clicking outside
    $(document).click(function(e) {
        if (!$(e.target).closest('.navbar').length) {
            $('.navbar-collapse').removeClass('show');
        }
    });
});

// Utility functions
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatDate(dateString) {
    var date = new Date(dateString);
    var now = new Date();
    var diff = now - date;
    var seconds = Math.floor(diff / 1000);
    var minutes = Math.floor(seconds / 60);
    var hours = Math.floor(minutes / 60);
    var days = Math.floor(hours / 24);
    
    if (days > 0) {
        return days + ' day' + (days > 1 ? 's' : '') + ' ago';
    } else if (hours > 0) {
        return hours + ' hour' + (hours > 1 ? 's' : '') + ' ago';
    } else if (minutes > 0) {
        return minutes + ' minute' + (minutes > 1 ? 's' : '') + ' ago';
    } else {
        return 'Just now';
    }
} 