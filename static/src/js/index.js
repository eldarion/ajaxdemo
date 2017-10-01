/* global window document */
window.jQuery = window.$ = require('jquery');

const $ = window.$;

window.Popper = require('popper.js');
require('bootstrap');
require('eldarion-ajax');
require('bootstrap-daterangepicker');

import moment from 'moment';
import ajaxSendMethod from './ajax';
import Sortable from 'sortablejs';

const loadDatePicker = () => {
    $('#id_date').daterangepicker({
        singleDatePicker: true,
        startDate: $('#id_date').val() || moment(),
        locale: {
            format: 'YYYY-MM-DD'
        }
    });
};

$(() => {
    $(document).ajaxSend(ajaxSendMethod);

    loadDatePicker();
    $(document).on('eldarion-ajax:complete', (event, $el, responseData, textStatus, jqXHR) => {
        if ($el.attr('id') === 'note-form' || $el.hasClass('note-edit-link')) {
          loadDatePicker();
        }
        if ($el.hasClass('note-edit-link')) {
          $el.parent().find('.note').toggleClass('active', false);
          $el.toggleClass('active');
        }
    });

    const $noteList = $('#note-list');
    if ($noteList.length > 0) {
      const saveUrl = $noteList.data('save-order-url');
      Sortable.create($noteList[0], {
        store: {
          get: sortable => {
            return [];
          },
          set: sortable => {
            $.ajax({
              url: saveUrl,
              method: 'post',
              data: {
                order: sortable.toArray().join('|')
              }
            });
          }
        }
      });
    }

    // Topbar active tab support
    $('.topbar li').removeClass('active');

    const classList = $('body').attr('class').split(/\s+/);
    $.each(classList, (index, item) => {
        const selector = `ul.nav li#tab_${item}`;
        $(selector).addClass('active');
    });

    $('#account_logout, .account_logout').click(e => {
        e.preventDefault();
        $('#accountLogOutForm').submit();
    });
});
