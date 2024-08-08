function resetUnv() {
    if (editMode && unvId) {
        resetChoise();
        btn = document.getElementById(btnId);
        btn.innerHTML = 'تعديل';

        let items1 = Array.prototype.slice.call(
            document.getElementsByClassName(unvId),
            0
        );
        $(`.${unvId}[data-toggle="datepicker"]`).datepicker('destroy');
        for (let i = 0; i < items1.length; i++) {
            if (items1[i].classList.contains('mul')) {
                items1[i].innerHTML =
                    originals[items1[i].getAttribute('name')][1];
                items1[i].setAttribute(
                    'value',
                    originals[items1[i].getAttribute('name')][0]
                );
                items1[i].className = `editable ${unvId} mul`;
            } else {
                items1[i].innerHTML = originals[items1[i].getAttribute('name')];
                items1[i].className = `editable ${unvId}`;
            }

            items1[i].setAttribute('contenteditable', 'false');
        }
        editMode = false;
        unvId = '';
        btnId = '';
        originals = {};
        $('#keyTips').addClass('d-none');

    }
}

async function editUnv(e, id, did) {
    console.log(id, did);
    if (editMode && unvId !== `unv-${id}`) {
        reset();
    }
    editMode = true;
    unvId = `unv-${id}`;
    btnId = `unveb-${id}`;
    let items1 = Array.prototype.slice.call(
        document.getElementsByClassName(unvId),
        0
    );

    if (e.target.innerHTML === 'تعديل') {
        e.target.innerHTML = 'حفظ';
        $(`.${unvId}[data-toggle="datepicker"]`).datepicker({
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
                ].className = `editable border border-dark rounded p-2 unv-${id} mul activee`;
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
                ].className = `editable border border-dark rounded p-2 unv-${id}`;
            }
        }
    } else if (e.target.innerHTML === 'حفظ') {
        const schema = {
            universityDegreeCollege: (str) => {
                return !validator.isEmpty(str);
            },
            universityDegreeUniversity: (str) => {
                return !validator.isEmpty(str);
            },
            universityDegreeSection: (str) => {
                return true;
            },
            universityDegreeYear: (str) => {
                return validator.matches(str, /^[0-9]{4}[-][0-9]{4}$/);
            },
            universityDegreeAverage: (str) => {
                return validator.isFloat(str, {
                    min: 60.0,
                    max: 100,
                });
            },
        };
        const errors = {
            freezeDecisionDate: 'تأكد من حقل تاريخ القرار',
            freezeDecisionNumber: 'تأكد من حقل رقم القرار',
            freezeDecisionType: 'تأكد من حقل نوع القرار',
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

            let status = await edit(values, id, did, 'unv'); 
            if(status === 'good'){

                for (let i = 0; i < items1.length; i++) {
                    if (items1[i].classList.contains('mul')) {
                        items1[i].className = `editable unv-${id} mul`;
                    } else {
                        items1[i].className = `editable unv-${id}`;
                    }
    
                    items1[i].setAttribute('contenteditable', 'false');
                }
                e.target.innerHTML = 'تعديل';
                $(`.${unvId}[data-toggle="datepicker"]`).datepicker('destroy');
                $('#keyTips').addClass('d-none');
    
                editMode = false;
                unvId = '';
                btnId = '';
                orignals = {};
            } else {
                resetUnv()
            }
            
        } else {
            values = {};
        }
    }
}
