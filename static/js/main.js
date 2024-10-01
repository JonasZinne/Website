// loading indicator
document.querySelector("form")?.addEventListener("submit", function() {
    document.getElementById("loadingIndicator").style.display = "flex";
});

// copy to clipboard
function copyToClipboard() {
    const textarea = document.getElementById("vetoResultsTextarea");
    
    let text = textarea.value.split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0) 
        .join('\n');

    navigator.clipboard.writeText(text)
        .then(() => {
            alert('Ergebnis wurde erfolgreich in die Zwischenablage kopiert.');
        })
        .catch(err => {
            alert('Fehler beim Kopieren: ' + err);
        });
}

// export vetos
document.addEventListener('DOMContentLoaded', function () {
    const teamSelects = document.querySelectorAll('.team-select');
    const mapSelects = document.querySelectorAll('.map-select');
    const divisionRadios = document.querySelectorAll('input[name="division"]');

    const numMatches = document.querySelectorAll('.veto-grid table').length;

    function updateURLParameter(param, value) {
        const url = new URL(window.location);
        url.searchParams.set(param, value);
        window.location.href = url;
    }

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
        for (let i = 0; i < numMatches; i++) {
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

    divisionRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            updateURLParameter('division', this.value);
        });
    });

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