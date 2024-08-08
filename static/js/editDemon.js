function resetDemon() {
    if (editMode && demonId) {
        resetChoise();
        btn = document.getElementById(btnId);
        btn.innerHTML = 'تعديل';

        let items1 = Array.prototype.slice.call(
            document.getElementsByClassName(demonId),
            0
        );

        $(`.${demonId}[data-toggle="datepicker"]`).datepicker('destroy');
        for (let i = 0; i < items1.length; i++) {
            if (items1[i].classList.contains('mul')) {
                items1[i].innerHTML =
                    originals[items1[i].getAttribute('name')][1];
                items1[i].setAttribute(
                    'value',
                    originals[items1[i].getAttribute('name')][0]
                );
                items1[i].className = `editable ${demonId} mul`;
            } else {
                items1[i].innerHTML = originals[items1[i].getAttribute('name')];
                items1[i].className = `editable ${demonId}`;
            }

            items1[i].setAttribute('contenteditable', 'false');
        }
        editMode = false;
        demonId = '';
        btnId = '';
        originals = {};
        $('#keyTips').addClass('d-none');
    }
}

async function editDemon(e, id) {
    if (editMode && demonId !== `demon-${id}`) {
        reset();
    }
    editMode = true;
    demonId = `demon-${id}`;
    btnId = `deb-${id}`;
    let items1 = Array.prototype.slice.call(
        document.getElementsByClassName(demonId),
        0
    );

    if (e.target.innerHTML === 'تعديل') {
        e.target.innerHTML = 'حفظ';
        $(`.${demonId}[data-toggle="datepicker"]`).datepicker({
            autoHide: true,
        });
        $('#keyTips').removeClass('d-none');

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
                ].className = `editable border border-dark rounded p-2 demon-${id} mul activee`;
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
                ].className = `editable border border-dark rounded p-2 demon-${id}`;
            }
        }
    } else if (e.target.innerHTML === 'حفظ') {
        const schema = {
            name: (str) => {
                return !validator.isEmpty(str);
            },
            fatherName: (str) => {
                return !validator.isEmpty(str);
            },
            motherName: (str) => {
                return !validator.isEmpty(str);
            },
            home: (str) => {
                return !validator.isEmpty(str);
            },
            residence: (str) => {
                return !validator.isEmpty(str);
            },
            mobile: (str) => {
                return (
                    !validator.isEmpty(str) &&
                    validator.matches(
                        str,
                        /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/
                    )
                );
            },
            telephone: (str) => {
                return (
                    validator.isEmpty(str) ||
                    validator.matches(str, /^([0-9]{3}[-]?)?[0-9]{7}$/)
                );
            },
            email: (str) => {
                return validator.isEmail(str);
            },
            birthDate: (str) => {
                return validator.isDate(str, { format: 'mm/dd/yyyy' });
            },
            gender: (str) => {
                return (
                    validator.equals(str, 'male') ||
                    validator.equals(str, 'female')
                );
            },
            currentAdjective: (str) => {
                return (
                    validator.equals(str, 'demonstrator') ||
                    validator.equals(str, 'returning') ||
                    validator.equals(str, 'envoy') ||
                    validator.equals(str, 'returning demonstrator') ||
                    validator.equals(str, 'loathes') ||
                    validator.equals(str, 'transfer outside the university') ||
                    validator.equals(str, 'end services') ||
                    validator.equals(str, 'resigned')
                );
            },
            maritalStatus: (str) => {
                return (
                    validator.equals(str, 'married') ||
                    validator.equals(str, 'unmarried')
                );
            },
            militarySituation: (str) => {
                return (
                    validator.equals(str, 'delayed') ||
                    validator.equals(str, 'laid off')
                );
            },
            university: (str) => {
                return !validator.isEmpty(str);
            },
            college: (str) => {
                return !validator.isEmpty(str);
            },
            section: (str) => {
                return true;
            },
            specialization: (str) => {
                return true;
            },
            commencementAfterNominationDate: (str) => {
                return (
                    validator.isEmpty(str) ||
                    validator.isDate(str, { format: 'mm/dd/yyyy' })
                );
            },
            language: (str) => {
                return !validator.isEmpty(str);
            },
            nominationDecisionNumber: (str) => {
                return !validator.isEmpty(str) && validator.isNumeric(str);
            },
            nominationDecisionType: (str) => {
                return (
                    validator.equals(str, 's') ||
                    validator.equals(str, 'o') ||
                    validator.equals(str, 'b')
                );
            },
            nominationDecisionDate: (str) => {
                return validator.isDate(str, { format: 'mm/dd/yyyy' });
            },
        };
        const errors = {
            name: 'تأكد من حقل الاسم',
            fatherName: 'تأكد من حقل اسم الأب',
            motherName: 'تأكد من حقل اسم الأم',
            home: 'تأكد من حقل مكان الإقامة',
            residence: 'تأكد من حقل العنوان الحالي',
            mobile: 'تأكد من رقم الهاتف المحمول',
            telephone: 'تأكد من رقم الهاتف الأرضي',
            email: 'تأكد من الإيميل',
            birthDate: 'تأكد من تاريخ الولادة',
            currentAdjective: 'تأكد من حقل الصفة الحالية',
            gender: 'تأكد من حقل الجنس',
            maritalStatus: 'تأكد من حقل الحالة الاجتماعية',
            militarySituation: 'تأكد من حقل الوضع العسكري',
            university: 'تأكد من حقل جامعة التعيين',
            college: 'تأكد من حقل كلية التعيين',
            commencementAfterNominationDate: 'تأكد من حقل المباشرة ',
            language: 'تأكد من حقل اللغة',
            nominationDecisionNumber: 'تأكد من حقل رقم القرار',
            nominationDecisionType: 'تأكد من حقل نوع القرار',
            nominationDecisionDate: 'تأكد من حقل تاريخ القرار',
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
            let status = await edit(values, id, 9, 'demon');

            if (status === 'good') {
                for (let i = 0; i < items1.length; i++) {
                    if (items1[i].classList.contains('mul')) {
                        items1[i].className = `editable demon-${id} mul`;
                    } else {
                        items1[i].className = `editable demon-${id}`;
                    }

                    items1[i].setAttribute('contenteditable', 'false');
                }

                $('#keyTips').addClass('d-none');
                e.target.innerHTML = 'تعديل';
                $(`.${demonId}[data-toggle="datepicker"]`).datepicker(
                    'destroy'
                );
                editMode = false;
                demonId = '';
                btnId = '';
                orignals = {};
            } else {
                resetDemon();
            }
        } else {
            values = {};
        }
    }
}
