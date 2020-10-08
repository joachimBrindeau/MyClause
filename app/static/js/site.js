window.onload = function(){

    const overlay = document.getElementById('search-overlay');
    const input = document.getElementById('search-input');
    const resultList = document.getElementById('result-list');
    const loader = document.getElementById('search-loader');
    const resultContainer = document.getElementById('result-container');

    const clauseIdField = document.getElementById('clause-id');
    const clauseTitleField = document.getElementById('title');
    const clauseTextField = document.getElementById('text');

    const saveAsNewBtn = document.getElementById('save-as-new');
    const saveBtn = document.getElementById('save-existing');
    const deleteBtn = document.getElementById('delete');
    const logoutBtn = document.getElementById('logout');

    // Checkboxes
    const privateClauses = document.getElementById('activate-own-search');
    const privateMode = document.getElementById('private-repo-check');

    // Debounce function
    function debounce(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };

    // Start loading animation, clear previous results
    function startLoading(){
        resultList.classList.add('visible');
        loader.classList.add('visible');
        
        resultContainer.classList.remove('visible');
    }

    // Binds result click to fetching information
    function bindSearchResults(){
        const results = document.getElementsByClassName('search-bar-results-result');

        for(let i = 0; i < results.length; i++){
            results[i].addEventListener('click', (ev) => {
                const targ = ev.currentTarget;
                const attr = targ.getAttribute('data-id')
                
                // Fetch the result and hide
                fetch(`api/clause/${attr}`)
                    .then(data => data.json())
                    .then(data => {
                        if(data['success']){
                            clauseIdField.value = data["id"]
                            clauseTitleField.value = data["title"]
                            clauseTextField.value = data["text"]
                        }
                    })
                    .then(deactivateSearch())
                    .catch(() => {
                        alert('Something went wrong');
                        deactivateSearch();
                    })
            })
        }
    }

    // Fill results, re-bind click events
    function finishLoading(results){
        resultContainer.innerHTML = results;
        
        bindSearchResults();
        
        loader.classList.remove('visible')
        resultContainer.classList.add('visible')
    }

    // Hide all results
    function hideResults(){
        resultList.classList.remove('visible')
    }

    function deactivateSearch(){
        hideResults();
        overlay.classList.remove('visible');
    }

    function clearFields(){
        clauseIdField.value = '';
        clauseTitleField.value = '';
        clauseTextField.value = '';
    }

    var inputDebounce = debounce(() => {

        // parse values
        let value = input.value;

        // Ensure there is a value, otherwise hide window
        if(value.length == 0){
            hideResults();
            return;
        }

        // start loading
        startLoading();

        fetch(`/api/search?q=${value}${privateClauses.checked?"&private=true":""}`)
            .then(data => data.json())
            .then(data => {
                if(data.count > 0){
                    finishLoading(data["result"])
                }else{
                    finishLoading("Nothing found..")
                }
            }).catch((reason) => {
                finishLoading([])
            })

    }, 250);

    input.addEventListener('input', inputDebounce);

    input.addEventListener('click', () => {
        overlay.classList.add('visible');
    })

    overlay.addEventListener('click', deactivateSearch)

    logoutBtn.addEventListener('click', () => {
        window.location.href = "/logout";
    })

    deleteBtn.addEventListener('click', () => {
        const val = clauseIdField.value
        if (val){
            fetch(`/api/delete/${val}`)
                .then(data => data.json())
                .then(data => {
                    if(data.message != ''){
                        alert(data.message);
                    }else{
                        alert('Succesfully deleted clause.')
                    }
                    clearFields();
                })
        }else{
            alert('Select a clause first.');
        }
    })

    saveAsNewBtn.addEventListener('click', () => {
        fetch('/api/save', {
            method: 'post',
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `clauseTitle=${clauseTitleField.value}&clauseText=${clauseTextField.value}${privateMode.checked?"&clausePrivate=true":""}`
        }).then((data) => data.json())
        .then(data => {
            if(data.success){
                alert("Successfully saved!")
            }else{
                alert(data.message)
            }
        })
    })

    saveBtn.addEventListener('click', () => {
        fetch('/api/save', {
            method: 'post',
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `clauseId=${clauseIdField.value}&clauseTitle=${clauseTitleField.value}&clauseText=${clauseTextField.value}${privateMode.checked?"&clausePrivate=true":""}`
        })
        .then((data) => data.json())
        .then(data => {
            if(data.success){
                alert("Successfully saved!")
            }else{
                alert(data.message)
            }
        })
    })
}

