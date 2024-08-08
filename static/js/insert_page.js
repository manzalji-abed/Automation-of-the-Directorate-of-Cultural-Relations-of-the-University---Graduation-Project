$(document).ready(function () {
    let hd = 1;
    let cd = 1;
    $('#state').change(function () {
        let str = '';
        $('#state option:selected').each(function () {
            str += $(this).text();
            if (str === 'مسابقة') {
                $('#state-father').after(
                    '<div class="col-12" id="added"><label for="cc-name" class="form-label">تاريخ إعلان المسابقة</label><input type="date" class="form-control" name="contestAnnouncementDate" required><div class="invalid-feedback">التاريخ مطلوب</div></div>'
                );
            } else {
                $('#added').remove();
            }
        });
    });

    $('#highC').click(function () {
        $(
            '#above-highc'
        ).before(`<div class="row" id="c${cd}"> <div class="row col-12 align-items-center justify-content-between"><h4 class="col-10 my-3 lead">شهادة تفوق </h4><button onclick="$('#c${cd}').remove()" type="button" class="btn btn-outline-danger col-1 btn-sm p-2 nothing" >x</button></div>
<div class="col-12 mb-2"><label class="form-label">الشهادة</label>
  <select
                    class="form-select"
                    
                    name="certificateOfExcellenceDegree"
                    required
                >
                    <option value="">اختر...</option>
                    <option value="1">الأول</option>
                    <option value="2">الثاني</option>
                    <option value="3">الثالث</option>
                </select>

    </div>
<div class="col-12">
    <label class="form-label">سنة الشهادة</label>
    <select
                    class="form-select"
                    
                    name="certificateOfExcellenceYear"
                    required
                >
                    <option value="">اختر...</option>
                    <option value="1">سنة أولى</option>
                    <option value="2">سنة ثانية</option>
                    <option value="3">سنة ثالثة</option>
                    <option value="4">سنة رابعة</option>
                    <option value="5">سنة خامسة</option>
                    <option value="6">سنة سادسة</option>
                    <option value="g">تخرج</option>
                </select>
    
</div></div>`);
        cd++;
    });

    $('#highD').click(function () {
        $('#above-highd').before(`
        
        <div class = "row" id="h${hd}">
            <div class="row col-12 align-items-center justify-content-between"><h4 class="lead my-3 col-10">شهادة دراسات عليا </h4><button onclick="$('#h${hd}').remove()" type="button" class="btn btn-outline-danger col-1 btn-sm p-2 nothing" >x</button></div>
            
        <div class="col-12 mb-3">
    <label class="form-label">الشهادة</label>
    <select
                    class="form-select"
                    
                    name="graduateStudiesDegree"
                    required
                >
                    <option value="">اختر...</option>
                    <option value="diploma">دبلوم</option>
                    <option value="master">ماجستير</option>
                    <option value="ph.d">دكتوراه</option>
                </select>
    
</div>
<div class="col-12 col-lg-6 mb-3">
    <label class="form-label">الجامعة</label>
    <input
        type="text"
        class="form-control"
        name="graduateStudiesUniversity"
        maxlength="50"
        required
    />
</div>
<div class="col-12 col-lg-6 mb-3">
    <label class="form-label">الكلية</label>
    <input
        type="text"
        class="form-control"
        name="graduateStudiesCollege"
        maxlength="50"
        required
    />
</div>
<div class="col-12 col-lg-6 mb-3">
    <label class="form-label">القسم</label>
    <input
        type="text"
        class="form-control"
        name="graduateStudiesSection"
        maxlength="50"
        required
    />
</div>
<div class="col-12 col-lg-6 mb-3">
    <label class="form-label">الاختصاص</label>
    <input
        type="text"
        class="form-control"
        name="graduateStudiesSpecialzaion"
        maxlength="50"
        required
    />
</div>
<div class="col-12 col-lg-6 mb-3">
    <label class="form-label">سنة الشهادة</label>
    <input
        type="text"
        class="form-control"
        name="graduateStudiesYear"
        pattern="^[0-9]{4}[-][0-9]{4}$"
                    placeholder="2018-2019"
        required
    />
    <div class="invalid-feedback">أدخل بتنسيق 2018-2019</div>
</div>
<div class="col-12 col-lg-6 mb-3">
    <label class="form-label">المعدل</label>
    <input
        type="number"
        min="60"
        max="100"
        step="0.001"
        class="form-control"
        name="graduateStudiesAverage"
        maxlength="50"
        required
    />
</div></div>`);
        hd++;
    });
});
