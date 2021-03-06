document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.elementsPerPage = 5;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
            this.populateSlide(this.elementsPerPage, 'foundations', 1);
            this.populateSlide(this.elementsPerPage, 'ngos', 2);
            this.populateSlide(this.elementsPerPage, 'local_donations', 3);
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        populateSlide(elPerPage, institutionType, slideDataId) {
            $.ajax({
                url: "/institutions/",
                type: "GET",

                success: function (json) {
                    const institutionArr = json[`${institutionType}`];
                    const ulElement = document.querySelector(`.help--slides[data-id="${slideDataId}"] ul`);
                    for (let i = 0; i < institutionArr.length; i++) {
                        const newClone = ulElement.firstElementChild.cloneNode(true);
                        let [name, description, categories] = institutionArr[i];
                        newClone.querySelector('.title').innerText = name;
                        newClone.querySelector('.subtitle').innerText = description;
                        newClone.querySelector('.text').innerText = categories;
                        if (i >= elPerPage) {
                            newClone.style.display = 'none'
                        }
                        ulElement.appendChild(newClone);
                    }
                    ulElement.firstElementChild.remove();


                    const ulPagination = document.querySelector(`.help--slides[data-id="${slideDataId}"] ul.help--slides-pagination`);
                    for (let i = 1; i <= Math.ceil(institutionArr.length / elPerPage); i++) {
                        const newClone = ulPagination.firstElementChild.cloneNode(true);
                        newClone.firstElementChild.dataset.page = i;
                        newClone.firstElementChild.innerText = i;
                        if (i === 1) {
                            newClone.firstElementChild.classList.add('active');
                        }
                        ulPagination.appendChild(newClone);
                    }
                    ulPagination.firstElementChild.remove();
                },

                error: function () {
                    console.log('something went wrong!');
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            // console.log(page);

            const slideId = e.target.parentElement.parentElement.parentElement.dataset.id;

            const liPagination = document.querySelectorAll(`div[data-id="${slideId}"] a`);
            liPagination.forEach(li => li.classList.remove('active'));
            e.target.classList.add('active');

            const ulContent = document.querySelector(`.help--slides[data-id="${slideId}"] ul`).children;
            const firstPageElIndex = this.elementsPerPage * (page - 1);
            for (let i = 0; i < ulContent.length; i++) {
                if (firstPageElIndex + this.elementsPerPage > i && i >= firstPageElIndex) {
                    ulContent[i].style.display = 'flex';
                } else {
                    ulContent[i].style.display = 'none';
                }
            }
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();

            $.ajax({
                url: "/add_donation/",
                type: "POST",
                data: $('form').serializeArray(),

                success: function (json) {
                    if (json['response']) {
                        window.location.replace("/confirmation_donation/");
                    } else {
                        console.log('the donation object was not saved')
                    }
                },

                error: function () {
                    console.log('something went wrong!');
                }
            });
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

    if (!!document.querySelector('[data-step="1"] .btn')) {
        $('[data-step="1"] .btn').click(function () {
            const categories = $('input[type=checkbox]:checked').map(function (_, el) {
                return $(el).val();
            }).get();

            const instDivs = document.querySelectorAll('[data-step="3"] .form-group--checkbox');
            instDivs.forEach(el => {
                el.style.display = 'block'
            });

            sendCategories();

            function sendCategories() {
                $.ajax({
                    url: "/filter_institutions/",
                    type: "GET",
                    data: {'categories_ids': JSON.stringify(categories)},

                    success: function (json) {

                        const previouslyAdded = document.querySelectorAll('[data-step="3"] .form-group--checkbox');
                        previouslyAdded.forEach(el => {
                            if (!el.querySelector('[value="old"]')) {
                                el.remove();
                            }
                        });

                        const instArr = json['filtered_ins'];
                        const btnDiv = document.querySelector('[data-step="3"] .form-group--buttons');
                        for (let i = 0; i < instArr.length; i++) {
                            const newClone = document.querySelector('[data-step="3"] .form-group--checkbox').cloneNode(true);
                            let [pk, name, description] = instArr[i];
                            newClone.querySelector('[name="organization"]').value = pk;
                            newClone.querySelector('.title').innerText = name;
                            newClone.querySelector('.subtitle').innerText = description;
                            btnDiv.parentNode.insertBefore(newClone, btnDiv)
                        }

                        document.querySelector('[value="old"]').parentElement.parentElement.style.display = 'none';
                    },

                    error: function () {
                        console.log('something went wrong!');
                    }
                });
            }
        });


        let formData;

        document.querySelector('[data-step="4"] .next-step').addEventListener('click', function () {

            formData = {};

            const categoriesArr = [];
            const categoriesVal = [];
            const categoriesDivs = document.querySelectorAll('[data-step="1"] .form-group--checkbox');
            categoriesDivs.forEach(el => {
                if (el.querySelector('input').checked) {
                    categoriesArr.push(el.querySelector('.description').innerText);
                    categoriesVal.push(el.querySelector('[name="categories"]').value);
                }
            });
            formData.categories = categoriesVal;


            const bagsVal = document.querySelector('[name="bags"]').value;
            formData.bags = bagsVal;
            const bagsCategorySummary = document.querySelector('[data-step="5"] .summary--text');
            bagsCategorySummary.innerText = `${bagsVal} worków z kategorii: ${categoriesArr.join(', ')}`;


            formData.organization = '';
            let organizationName;
            let organizationDivs = document.querySelectorAll('[data-step="3"] .form-group--checkbox');
            organizationDivs.forEach(el => {
                if (el.querySelector('input').checked) {
                    organizationName = el.querySelector('.title').innerText;
                    formData.organization = el.querySelector('[name="organization"]').value;
                }
            });
            const organizationSummary = document.querySelector('[data-step="5"] li:nth-child(2) .summary--text');
            organizationSummary.innerText = `Dla fundacji ${organizationName}`;


            const address = document.querySelector('[name="address"]').value;
            const addressSummary = document.querySelector('[data-step="5"] .form-section.form-section--columns li');
            addressSummary.innerText = address;
            formData.address = address;


            const city = document.querySelector('[name="city"]').value;
            const citySummary = document.querySelector('[data-step="5"] .form-section.form-section--columns li:nth-child(2)');
            citySummary.innerText = city;
            formData.city = city;


            const postcode = document.querySelector('[name="postcode"]').value;
            const postcodeSummary = document.querySelector('[data-step="5"] .form-section.form-section--columns li:nth-child(3)');
            postcodeSummary.innerText = postcode;
            formData.postcode = postcode;


            const phone = document.querySelector('[name="phone"]').value;
            const phoneSummary = document.querySelector('[data-step="5"] .form-section.form-section--columns li:nth-child(4)');
            phoneSummary.innerText = phone;
            formData.phone = phone;


            const data = document.querySelector('[name="data"]').value;
            const dataSummary = document.querySelectorAll('[data-step="5"] .form-section--column')[1].querySelector('li');
            dataSummary.innerText = data;
            formData.data = data;


            const time = document.querySelector('[name="time"]').value;
            const timeSummary = document.querySelectorAll('[data-step="5"] .form-section--column')[1].querySelector('li:nth-child(2)');
            timeSummary.innerText = time;
            formData.time = time;


            const moreInfo = document.querySelector('[name="more_info"]').value;
            const moreInfoSummary = document.querySelectorAll('[data-step="5"] .form-section--column')[1].querySelector('li:nth-child(3)');
            moreInfoSummary.innerText = moreInfo;
            formData.more_info = moreInfo;
        });
    }


    function changeTable() {
        const donationTr = document.querySelectorAll('tbody tr');
        donationTr.forEach(tr => {
                if (tr.lastElementChild.firstElementChild.firstElementChild.checked) {
                    const toChange = tr.querySelectorAll('td').forEach(td => td.style.color = 'lightgray');
                } else {
                    tr.querySelectorAll('td').forEach(td => td.style.color = '#333')
                }
            }
        )
    }

    changeTable();

    const isTaken = document.querySelectorAll('tbody tr td:last-child [type="radio"]');

    isTaken.forEach(input => input.addEventListener("change", function (evt) {

        $.ajax({
            url: "/profile/",
            type: "POST",
            data: $('form').serializeArray(),

            success: function (json) {
                if (json['response']) {
                    // console.log('changed');
                    changeTable();
                } else {
                    alert('NIE zmieniono');
                    location.reload();
                }
            },

            error: function () {
                console.log('something went wrong!');
                alert('NIE zmieniono');
                location.reload();
            }
        });
    }));

});
