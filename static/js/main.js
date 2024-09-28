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
    const teamSelects = document.querySelectorAll('.team-select');
    const mapSelects = document.querySelectorAll('.map-select');
    const divisionRadios = document.querySelectorAll('input[name="division"]');

    function updateTeams(division) {
        fetch('/get_teams', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ division: division })
        })
        .then(response => response.json())
        .then(data => {
            const teams = data.teams;

            teamSelects.forEach(select => {
                const currentValue = select.value;
                select.innerHTML = '<option value="" disabled selected hidden>Bitte wählen</option>';

                teams.forEach(team => {
                    const option = document.createElement('option');
                    option.value = team;
                    option.textContent = team;
                    select.appendChild(option);
                });

                if (teams.includes(currentValue)) {
                    select.value = currentValue;
                }
            });

            updateTeamSelectOptions();
            updateMapSelectOptions();
        })
        .catch(error => console.error('Error:', error));
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

    divisionRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                updateTeams(this.value);
            }
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

    function init() {
        const selectedDivision = document.querySelector('input[name="division"]:checked').value;
        updateTeams(selectedDivision);
        updateTeamSelectOptions();
        updateMapSelectOptions();
    }

    // Initialisierung
    init();

    document.getElementById('copyButton')?.addEventListener('click', copyToClipboard);
});