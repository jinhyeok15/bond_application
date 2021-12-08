let filterStatus = 0;
const RATING_TYPE = [
    '국고채', 'AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-'
]
$(document).ready(function(){
    $('#content-filter-box-button').on('click', function() {
        if (filterStatus===0) {
            $('#content-filter-box').addClass('active');
            $('#content-filter-list').addClass('active');
            $('.selected-type').addClass('active');
            filterStatus=1;
        }
        else {
            $('#content-filter-box').removeClass('active');
            $('#content-filter-list').scrollTop(0);
            $('#content-filter-list').removeClass('active');
            $('.selected-type').removeClass('active');
            filterStatus=0;
        }
    });
    
    RATING_TYPE.forEach(function(value, index, array){
        $(`#${value}`).on('click', function() {
        $('#content-filter-box').removeClass('active');
        $('#content-filter-list').scrollTop(0);
        $('#content-filter-list').removeClass('active');
        $('.selected-type').removeClass('active');
        filterStatus=0;
    });
    });
});