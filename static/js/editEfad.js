let g;

function resetEfad() {
    if (editMode && efadId) {
        resetChoise();
        btn = document.getElementById(btnId);
        textarea = document.getElementById(`EfadfloatingText-${g}`);
        console.log(`EfadfloatingText-${efadId}`);
        textarea.setAttribute('disabled', 'true');
        btn.innerHTML = 'تعديل';
        $(`#requiredCertificateo`).addClass('d-none');

        let items1 = Array.prototype.slice.call(
            document.getElementsByClassName(efadId),
            0
        );
        $(`.${efadId}[data-toggle="datepicker"]`).datepicker('destroy');
        for (let i = 0; i < items1.length; i++) {
            if (items1[i].classList.contains('mul')) {
                items1[i].innerHTML =
                    originals[items1[i].getAttribute('name')][1];
                items1[i].setAttribute(
                    'value',
                    originals[items1[i].getAttribute('name')][0]
                );
                items1[i].className = `editable ${efadId} mul`;
            } else {
                items1[i].innerHTML = originals[items1[i].getAttribute('name')];
                items1[i].className = `editable ${efadId}`;
            }

            items1[i].setAttribute('contenteditable', 'false');
        }
        editMode = false;
        efadId = '';
        btnId = '';
        originals = {};
        $('#keyTips').addClass('d-none');
    }
}

async function editEfad(e, id, did) {
    if (editMode && efadId !== `efad-info-${id}`) {
        reset();
    }
    editMode = true;
    efadId = `efad-info-${id}`;
    btnId = `efeb-${id}`;
    g = id;
    textarea = document.getElementById(`EfadfloatingText-${id}`);
    let items1 = Array.prototype.slice.call(
        document.getElementsByClassName(efadId),
        0
    );

    if (e.target.innerHTML === 'تعديل') {
        e.target.innerHTML = 'حفظ';
        $('#keyTips').removeClass('d-none');

        $(`.${efadId}[data-toggle="datepicker"]`).datepicker({
            autoHide: true,
        });
        $(`#requiredCertificateo`).removeClass('d-none');
        textarea.removeAttribute('disabled');
        for (let i = 0; i < items1.length; i++) {
            originals[items1[i].getAttribute('name')] = items1[i].innerHTML;
            items1[i].setAttribute('contenteditable', 'true');
            if (items1[i].classList.contains('mul')) {
                originals[items1[i].getAttribute('name')] = [
                    items1[i].getAttribute('value'),
                    items1[i].innerHTML,
                ];
                items1[
                    i
                ].className = `editable border border-dark rounded p-2 efad-info-${id} mul activee`;
                $(`.activee`).on({
                    focusin: function () {
                        $(
                            `~ .${items1[i].getAttribute('name')}`,
                            this
                        ).removeClass('d-none');
                        $(this).addClass('changeable');
                    },
                    blur: function () {
                        $(
                            `~ .${items1[i].getAttribute('name')}`,
                            this
                        ).addClass('d-none');
                        $(this).removeClass('changeable');
                    },
                });

                $(
                    `.activee + .${items1[i].getAttribute('name')} > div`
                ).mousedown(function () {
                    $(`.changeable`)
                        .text($('> strong', this).text())
                        .attr('value', $('> strong', this).attr('value'));
                });
            } else {
                items1[
                    i
                ].className = `editable border border-dark rounded p-2 efad-info-${id}`;
            }
        }
    } else if (e.target.innerHTML === 'حفظ') {
        const schema = {
            requiredCertificate: (str) => {
                return (
                    validator.equals(str, 'language') ||
                    validator.equals(str, 'master') ||
                    validator.equals(str, 'ph.d')
                );
            },
            alimony: (str) => {
                return (
                    validator.equals(str, 'grant') ||
                    validator.equals(str, 'seat')
                );
            },
            commencementDate: (str) => {
                return (
                    validator.isEmpty(str) ||
                    validator.isDate(str, { format: 'mm/dd/yyyy' })
                );
            },
            dispatchEndDate: (str) => {
                return (
                    validator.isEmpty(str) ||
                    validator.isDate(str, { format: 'mm/dd/yyyy' })
                );
            },
            backDate: (str) => {
                return (
                    validator.isEmpty(str) ||
                    validator.isDate(str, { format: 'mm/dd/yyyy' })
                );
            },
            defenseDate: (str) => {
                return (
                    validator.isEmpty(str) ||
                    validator.isDate(str, { format: 'mm/dd/yyyy' })
                );
            },
            gettingCertificateDate: (str) => {
                return (
                    validator.isEmpty(str) ||
                    validator.isDate(str, { format: 'mm/dd/yyyy' })
                );
            },
            atDisposalOfUniversityDate: (str) => {
                return (
                    validator.isEmpty(str) ||
                    validator.isDate(str, { format: 'mm/dd/yyyy' })
                );
            },
            dispatchCountry: (str) => {
                return validator.isLength(str, { min: 1, max: 256 });
            },
            dispatchDecisionDate: (str) => {
                return validator.isDate(str, { format: 'mm/dd/yyyy' });
            },
            dispatchDecisionNumber: (str) => {
                return !validator.isEmpty(str) && validator.isNumeric(str);
            },
            dispatchDecisionType: (str) => {
                return (
                    validator.equals(str, 's') ||
                    validator.equals(str, 'o') ||
                    validator.equals(str, 'b')
                );
            },
            dispatchType: (str) => {
                return (
                    validator.equals(str, 'inner') ||
                    validator.equals(str, 'outer')
                );
            },
            dispatchUniversity: (str) => {
                return validator.isLength(str, { min: 1, max: 256 });
            },
            innerSupervisor: (str) => {
                return validator.isLength(str, { min: 1, max: 256 });
            },
            lastReportDate: (str) => {
                return true;
            },
            outerSupervisor: (str) => {
                return validator.isLength(str, { min: 1, max: 256 });
            },
            dispatchDurationYear: (str) => {
                return validator.isInt(str);
            },
            dispatchDurationMonth: (str) => {
                return validator.isInt(str);
            },
            dispatchDurationDay: (str) => {
                return validator.isInt(str);
            },
        };
        const errors = {
            requiredCertificate: 'تأكد من حقل الشهادة المطلوبة',
            alimony: 'تأكد من حقل النفقة',
            commencementDate: 'تأكد من حقل تاريخ المباشرة',
            dispatchEndDate: 'تأكد من حقل تاريخ انتهاء الإيفاد',
            backDate: 'تأكد من حقل تاريخ العودة',
            defenseDate: 'تأكد من حقل تاريخ الدفاع',
            gettingCertificateDate: 'تأكد من حقل تاريخ الحصول على الشهادة',
            atDisposalOfUniversityDate:
                'تأكد من حقل تاريخ الوضع تحت تصرف الجامعة',
            dispatchCountry: 'تأكد من حقل بلد الإيفاد',
            dispatchDecisionDate: 'تأكد من حقل تاريخ القرار',
            dispatchDecisionNumber: 'تأكد من حقل رقم القرار',
            dispatchDecisionType: 'تأكد من حقل نوع القرار',
            dispatchType: 'تأكد من حقل نوع الإيفاد',
            dispatchUniversity: 'تأكد من حقل جامعة الإيفاد',
            innerSupervisor: 'تأكد من حقل المشرف الداخلي',
            outerSupervisor: 'تاكد من حقل المشرف الخارجي',
            dispatchDurationYear: 'تأكد أن الحقل يحتوي على عدد صحيح',
            dispatchDurationMonth: 'تأكد أن الحقل يحتوي على عدد صحيح',
            dispatchDurationDay: 'تأكد أن الحقل يحتوي على عدد صحيح',
        };

        let df = true;

        let values = {};
        for (let i = 0; i < items1.length; i++) {
            values[items1[i].getAttribute('name')] = items1[i].innerHTML;
            if (items1[i].hasAttribute('value')) {
                values[items1[i].getAttribute('name')] =
                    items1[i].getAttribute('value');
            }
            if (
                !schema[items1[i].getAttribute('name')](
                    values[items1[i].getAttribute('name')]
                )
            ) {
                df = false;
                window.alert(errors[items1[i].getAttribute('name')]);
                break;
            }
        }
        if (df) {
            console.log(values);
            values['csrfmiddlewaretoken'] = csrf.value;
            values['dispatchNotes'] = textarea.value;

            let status = await edit(values, id, did, 'efad');

            if (status === 'good') {
                textarea.setAttribute('disabled', 'true');

                for (let i = 0; i < items1.length; i++) {
                    if (items1[i].classList.contains('mul')) {
                        items1[i].className = `editable efad-info-${id} mul`;
                    } else {
                        items1[i].className = `editable efad-info-${id}`;
                    }

                    items1[i].setAttribute('contenteditable', 'false');
                }
                $(`#requiredCertificateo`).addClass('d-none');
                $(`#requiredCertificate`).text(
                    $(`.${efadId}[name=requiredCertificate]`).text()
                );

                e.target.innerHTML = 'تعديل';
                $(`.${efadId}[data-toggle="datepicker"]`).datepicker('destroy');
                $('#keyTips').addClass('d-none');

                editMode = false;
                efadId = '';
                btnId = '';
                orignals = {};
            } else {
                resetEfad();
            }
        } else {
            values = {};
        }
    }
}
