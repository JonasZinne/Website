// loading indicator
document.querySelector("form").addEventListener("submit", function() {
    document.getElementById("loadingIndicator").style.display = "flex";
});

// export matches
function copyToClipboard() {
    const textarea = document.getElementById("vetoResultsTextarea");
    
    let text = textarea.value.split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0) 
        .join('\n');

    navigator.clipboard.writeText(text)
        .catch(err => {
            alert('Fehler beim Kopieren: ' + err);
        });
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('copyButton').addEventListener('click', copyToClipboard);

    const teamSelects = document.querySelectorAll('.team-select');
    const mapSelects = document.querySelectorAll('.map-select');

    function updateTeamSelectOptions() {
        const selectedTeams = Array.from(teamSelects)
            .map(select => select.value)
            .filter(value => value);
        
        teamSelects.forEach(select => {
            const currentValue = select.value;
            Array.from(select.options).forEach(option => {
                option.disabled = selectedTeams.includes(option.value) && option.value !== currentValue;
            });
        });
    }

    function updateMapSelectOptions() {
        for (let i = 0; i < 4; i++) {
            const mapSelects = document.querySelectorAll('.map-select-' + i);

            const selectedMaps = Array.from(mapSelects)
                .map(select => select.value)
                .filter(value => value);

            mapSelects.forEach(select => {
                const currentValue = select.value;
                Array.from(select.options).forEach(option => {
                    option.disabled = selectedMaps.includes(option.value) && option.value !== currentValue;
                });
            });
        }
    }

    teamSelects.forEach(select => {
        select.addEventListener('change', function() {
            updateTeamSelectOptions();
            updateMapSelectOptions();
        });
    });

    mapSelects.forEach(select => {
        select.addEventListener('change', updateMapSelectOptions);
    });

    updateTeamSelectOptions();
    updateMapSelectOptions();
});