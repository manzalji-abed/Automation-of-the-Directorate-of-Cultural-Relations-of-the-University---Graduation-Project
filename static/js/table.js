import Fuse from './fuse.esm.js';

const templater = document.createElement('template');
templater.innerHTML = `
<style>
@import "/static/bootstrap-5.2.0/dist/css/bootstrap.rtl.min.css";
@import "/static/fontawesome-free-6.2.1-web/css/all.css";
table{
    background-color: #f9f9fc
}
button{
    width: 100px
}
tr,th{
    cursor:pointer 
}
</style>
`;

class DataTabler extends HTMLElement {
    constructor() {
        super();

        if (this.hasAttribute('src')) this.src = this.getAttribute('src');
        // If no source, do nothing
        if (!this.src) return;

        // attributes to do, datakey
        if (this.hasAttribute('cols'))
            this.cols = this.getAttribute('cols').split(',');

        this.pageSize = 10;
        if (this.hasAttribute('pagesize'))
            this.pageSize = this.getAttribute('pagesize');

        // helper values for sorting and paging
        this.sortAsc = false;
        this.curPage = 1;
        this.df = [];
        const shadow = this.attachShadow({
            mode: 'open',
        });
        this.shadowRoot.appendChild(templater.content.cloneNode(true));
        const div1 = document.createElement('div');
        const table = document.createElement('table');
        table.classList.add('table', 'table-hover');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');
        tbody.classList.add('table-group-divider');
        const input = document.createElement('input');
        const select = document.createElement('select');
        select.classList.add('form-select');
        const option1 = document.createElement('option');
        option1.value = 'fields.name';
        option1.text = 'الاسم';
        option1.setAttribute('selected', 'selected');
        select.add(option1);
        const option2 = document.createElement('option');
        option2.value = 'fields.fatherName';
        option2.text = 'اسم الأب';
        select.add(option2);

        const option3 = document.createElement('option');
        option3.value = 'fields.motherName';
        option3.text = 'اسم الأم';
        select.add(option3);

        const option5 = document.createElement('option');
        option5.value = 'fields.university';
        option5.text = 'الجامعة';
        select.add(option5);
        const option6 = document.createElement('option');
        option6.value = 'fields.specialization';
        option6.text = 'التخصص';
        select.add(option6);

        const option4 = document.createElement('option');
        option4.value = 'fields.college';
        option4.text = 'الكلية';
        select.add(option4);

        input.classList.add('form-control');
        const i = document.createElement('i');
        i.classList.add('fa-sharp', 'fa-solid', 'fa-magnifying-glass');
        table.append(thead, tbody);

        const nav = document.createElement('div');
        nav.classList.add('px-3');
        const prevButton = document.createElement('button');
        prevButton.classList.add('btn', 'btn-outline-primary');
        prevButton.innerHTML = 'السابق';
        const nextButton = document.createElement('button');
        nextButton.classList.add('btn', 'btn-outline-primary', 'mx-2');
        nextButton.innerHTML = 'التالي';
        nav.append(prevButton, nextButton);

        const div2 = document.createElement('div');
        const div3 = document.createElement('div');
        const div4 = document.createElement('div');
        div4.classList.add('col-7');
        const div5 = document.createElement('div');
        div5.classList.add('col-3');
        div3.classList.add('row', 'mb-3');
        div2.classList.add('input-group');
        const span = document.createElement('span');
        span.classList.add('input-group-text');
        select.classList.add('col-3');

        span.append(i);

        div2.append(span, input);
        div4.append(div2);
        div5.append(select);
        div3.append(div4, div5);

        div1.append(div3, table);
        div1.classList.add('px-3');

        shadow.append(div1, nav);

        // Attach the created elements to the shadow dom

        // https://www.freecodecamp.org/news/this-is-why-we-need-to-bind-event-handlers-in-class-components-in-react-f7ea1a6f93eb/
        this.sort = this.sort.bind(this);

        this.nextPage = this.nextPage.bind(this);
        this.previousPage = this.previousPage.bind(this);
        this.search = this.search.bind(this);
        this.changeSearch = this.changeSearch.bind(this);

        this.options = {
            includeScore: true,
            keys: [select.value],
        };
        select.addEventListener('change', this.changeSearch, false);
        nextButton.addEventListener('click', this.nextPage, false);
        prevButton.addEventListener('click', this.previousPage, false);
    }

    load() {
        // error handling needs to be done :|
        this.data = JSON.parse(this.src);
        this.df = this.data;

        this.render();
    }

    nextPage() {
        if (this.curPage * this.pageSize < this.data.length) this.curPage++;
        this.renderBody();
    }

    previousPage() {
        if (this.curPage > 1) this.curPage--;
        this.renderBody();
    }

    render() {
        if (!this.cols) this.cols = Object.keys(this.data[0]['fields']);

        this.renderHeader();
        this.renderBody();
    }

    renderBody() {
        let result = '';
        let counter = 1;
        this.data
            .filter((row, index) => {
                let start = (this.curPage - 1) * this.pageSize;
                let end = this.curPage * this.pageSize;
                if (index >= start && index < end) return true;
            })
            .forEach((c) => {
                let r = `<tr onclick="window.location.assign('/app/demonstrator/${c['pk']}')">`;
                r += `<td>${counter}</td>`;
                counter++;
                this.cols.forEach((col) => {
                    r += `<td>${c['fields'][col] ? c['fields'][col] : ''}</td>`;
                });
                r += '</tr>';
                result += r;
            });

        let tbody = this.shadowRoot.querySelector('tbody');
        tbody.innerHTML = result;
        if (this.df.length <= 10) {
            let buttons = this.shadowRoot.querySelectorAll('button');
            buttons[0].classList.add('d-none');
            buttons[1].classList.add('d-none');
        }
    }

    renderHeader() {
        let header = '<tr>';
        header += `<th scope='col' data-sort="id">#</th>`;
        header += `<th scope='col' data-sort="name">الاسم</th>`;
        header += `<th scope='col' data-sort="fatherName">اسم الأب</th>`;
        header += `<th scope='col' data-sort="motherName">اسم الأم</th>`;
        header += `<th scope='col' data-sort="college">الجامعة</th>`;
        header += `<th scope='col' data-sort="college">الكلية</th>`;
        header += `<th scope='col' data-sort="college">التخصص</th>`;
        header += '</tr>';
        let thead = this.shadowRoot.querySelector('thead');
        thead.innerHTML = header;

        this.shadowRoot.querySelectorAll('thead tr th').forEach((t) => {
            t.addEventListener('click', this.sort, false);
        });
        this.shadowRoot
            .querySelector('input')
            .addEventListener('input', this.search, false);
    }

    search(e) {
        const fuse = new Fuse(this.data, this.options);

        const result = fuse.search(e.target.value);
        this.data = result.map((r) => r.item);
        if (!e.target.value) {
            this.data = this.df;
        }
        this.renderBody();
    }

    searchAfter() {
        const fuse = new Fuse(this.df, this.options);
        let sr = this.shadowRoot.querySelector('input').value;
        const result = fuse.search(sr);
        this.data = result.map((r) => r.item);
        if (!sr) {
            this.data = this.df;
        }
        this.renderBody();
    }

    changeSearch(e) {
        this.options.keys = [e.target.value];
        this.searchAfter();
    }

    async sort(e) {
        let thisSort = e.target.dataset.sort;

        if (this.sortCol && this.sortCol === thisSort)
            this.sortAsc = !this.sortAsc;
        this.sortCol = thisSort;
        if (this.sortCol === 'id') {
            this.data.sort((a, b) => {
                if (a['pk'] < b['pk']) return this.sortAsc ? 1 : -1;
                if (a['pk'] > b['pk']) return this.sortAsc ? -1 : 1;
                return 0;
            });
        } else {
            this.data.sort((a, b) => {
                if (a['fields'][this.sortCol] < b['fields'][this.sortCol])
                    return this.sortAsc ? 1 : -1;
                if (a['fields'][this.sortCol] > b['fields'][this.sortCol])
                    return this.sortAsc ? -1 : 1;
                return 0;
            });
        }

        this.renderBody();
    }

    static get observedAttributes() {
        return ['src'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        // even though we only listen to src, be sure
        if (name === 'src') {
            this.src = newValue;
            this.load();
        }
    }
}

// Define the new element
customElements.define('data-table', DataTabler);
