function resetGrad() {
    if (editMode && gradId) {
        resetChoise();
        btn = document.getElementById(btnId);
        btn.innerHTML = 'تعديل';

        let items1 = Array.prototype.slice.call(
            document.getElementsByClassName(gradId),
            0
        );
        $(`.${gradId}[data-toggle="datepicker"]`).datepicker('destroy');
        for (let i = 0; i < items1.length; i++) {
            if (items1[i].classList.contains('mul')) {
                items1[i].innerHTML =
                    originals[items1[i].getAttribute('name')][1];
                items1[i].setAttribute(
                    'value',
                    originals[items1[i].getAttribute('name')][0]
                );
                items1[i].className = `editable ${gradId} mul`;
            } else {
                items1[i].innerHTML = originals[items1[i].getAttribute('name')];
                items1[i].className = `editable ${gradId}`;
            }

            items1[i].setAttribute('contenteditable', 'false');
        }
        editMode = false;
        gradId = '';
        btnId = '';
        originals = {};
        $('#keyTips').addClass('d-none');
    }
}

async function editGrad(e, id, did) {
    console.log(id, did);
    if (editMode && gradId !== `grad-${id}`) {
        reset();
    }
    editMode = true;
    gradId = `grad-${id}`;
    btnId = `gradeb-${id}`;
    let items1 = Array.prototype.slice.call(
        document.getElementsByClassName(gradId),
        0
    );

    if (e.target.innerHTML === 'تعديل') {
        e.target.innerHTML = 'حفظ';
        $(`.${gradId}[data-toggle="datepicker"]`).datepicker({
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
                ].className = `editable border border-dark rounded p-2 grad-${id} mul activee`;
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
                ].className = `editable border border-dark rounded p-2 grad-${id}`;
            }
        }
    } else if (e.target.innerHTML === 'حفظ') {
        const schema = {
            graduateStudiesDegree: (str) => {
                return (
                    validator.equals(str, 'diploma') ||
                    validator.equals(str, 'master') ||
                    validator.equals(str, 'ph.d')
                );
            },
            graduateStudiesUniversity: (str) => {
                return !validator.isEmpty(str);
            },
            graduateStudiesSpecialzaion: (str) => {
                return !validator.isEmpty(str);
            },
            graduateStudiesCollege: (str) => {
                return !validator.isEmpty(str);
            },
            graduateStudiesSection: (str) => {
                return true;
            },
            graduateStudiesYear: (str) => {
                return validator.matches(str, /^[0-9]{4}[-][0-9]{4}$/);
            },
            graduateStudiesAverage: (str) => {
                return validator.isFloat(str, {
                    min: 60.0,
                    max: 100,
                });
            },
        };
        const errors = {
            graduateStudiesDegree: 'تأكد من حقل الشهادة',
            graduateStudiesUniversity: 'تأكد من حقل الجامعة',
            graduateStudiesSpecialzaion: 'تأكد من حقل التخصص',
            graduateStudiesCollege: 'تأكد من حقل الكلية',
            graduateStudiesSection: 'تأكد من حقل القسم',
            graduateStudiesYear: 'تأكد من حقل سنة التخرج',
            graduateStudiesAverage: 'تأكد من حقل المعدل',
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

            let status = await edit(values, id, did, 'grad');
            if (status === 'good') {
                for (let i = 0; i < items1.length; i++) {
                    if (items1[i].classList.contains('mul')) {
                        items1[i].className = `editable grad-${id} mul`;
                    } else {
                        items1[i].className = `editable grad-${id}`;
                    }

                    items1[i].setAttribute('contenteditable', 'false');
                }
                e.target.innerHTML = 'تعديل';
                $(`.${gradId}[data-toggle="datepicker"]`).datepicker('destroy');
                $('#keyTips').addClass('d-none');

                editMode = false;
                gradId = '';
                btnId = '';
                orignals = {};
            } else {
                resetGrad();
            }
        } else {
            values = {};
        }
    }
}
