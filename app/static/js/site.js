window.onload = function(){

    const overlay = document.getElementById('search-overlay');
    const input = document.getElementById('search-input');
    const resultList = document.getElementById('result-list');
    const loader = document.getElementById('search-loader');
    const resultContainer = document.getElementById('result-container');

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

    // Fill results, re-bind click events
    function finishLoading(results){
        resultContainer.innerHTML = results;
        loader.classList.remove('visible')
        resultContainer.classList.add('visible')
    }

    // Hide all results
    function hideResults(){
        resultList.classList.remove('visible')
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
                }
            }).catch((reason) => {
                finishLoading([])
            })

    }, 250);

    input.addEventListener('input', inputDebounce);

    input.addEventListener('click', () => {
        overlay.classList.add('visible');
    })

    overlay.addEventListener('click', () => {
        hideResults();
        overlay.classList.remove('visible');
    })
}

