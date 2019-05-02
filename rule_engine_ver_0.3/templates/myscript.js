var basic_filters = [
    {
        id: 'browser_id',
        label: 'Browser ID',
        type: 'string'
    },{
        id: 'category',
        label: 'Category',
        type: 'integer',
        validation: {
            min: 0
        },
        description: 'Lorem ipsum sit amet'
    },{
        id: 'region',
        label: 'Region',
        type: 'integer',
        validation: {
            min: 0
        },
    },{
        id: 'event_date',
        label: 'Event Date',
        type: 'date',
        validation: {
          format: 'YYYY/MM/DD'
        },
        plugin: 'datepicker',
        plugin_config: {
          format: 'yyyy/mm/dd',
          todayBtn: 'linked',
          todayHighlight: true,
          autoclose: true
        }
    },{
        id: 'tstamp',
        label: 'Timestamp',
        type: 'time'
    }
];

function transform_me(s) {
    return s.toUpperCase();
}

$(function() {
    var $b = $('#builder');

    $('#builder').queryBuilder({
        filters: basic_filters
    });
});

var rules_basic = {
    condition: 'AND',
    rules: [{
      id: 'price',
      operator: 'less',
      value: 10.25
    }, {
      condition: 'OR',
      rules: [{
        id: 'category',
        operator: 'equal',
        value: 2
      }, {
        id: 'category',
        operator: 'equal',
        value: 1
      }]
    }]
  };

  $('#btn-reset').on('click', function() {
    $('#builder-basic').queryBuilder('reset');
  });
  
  $('#btn-set').on('click', function() {
    $('#builder-basic').queryBuilder('setRules', rules_basic);
  });
  
  $('#btn-get').on('click', function() {
    var result = $('#builder').queryBuilder('getRules');
    console.log(JSON.stringify(result, null, 2))
    if (!$.isEmptyObject(result)) {
      // alert(JSON.stringify(result, null, 2));
      prompt("Copy to clipboard: Ctrl+C, Enter", JSON.stringify(result, null, 2));
    }
  });