from flask import Flask, request, render_template_string
from itertools import combinations

app = Flask(__name__)


# ============================================================
# SAMPLE BREEDING DATA
# ============================================================

DEFAULT_CANDIDATES = [
    {
        "name": "P1",
        "traits": [
            "High Yield",
            "Disease Resistance",
            "Fast Growth"
        ]
    },
    {
        "name": "P2",
        "traits": [
            "Medium Yield",
            "Disease Resistance",
            "Fast Growth"
        ]
    },
    {
        "name": "P3",
        "traits": [
            "High Yield",
            "Fast Growth"
        ]
    },
    {
        "name": "P4",
        "traits": [
            "High Yield",
            "Disease Resistance",
            "Medium Growth"
        ]
    }
]


# ============================================================
# HTML + CSS + JAVASCRIPT
# ============================================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Genetic Trait Combination Solver
</title>


<style>

/* =========================================================
   GENERAL
========================================================= */

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f4f7fb;
    color: #1f2937;
}


/* =========================================================
   HEADER
========================================================= */

.header {
    background: linear-gradient(
        135deg,
        #173f5f,
        #20639b
    );

    color: white;

    padding: 45px 20px;

    text-align: center;
}

.header h1 {
    margin: 0;

    font-size: 38px;
}

.header p {
    margin: 10px 0 0;

    font-size: 17px;
}


/* =========================================================
   CONTAINER
========================================================= */

.container {
    max-width: 1150px;

    margin: 30px auto;

    padding: 0 20px;
}


/* =========================================================
   CARDS
========================================================= */

.card {
    background: white;

    border-radius: 15px;

    padding: 25px;

    margin-bottom: 25px;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.08);
}

.card h2 {
    margin-top: 0;
}


/* =========================================================
   CANDIDATE INPUT
========================================================= */

.candidate {
    display: grid;

    grid-template-columns:
        1fr 2fr auto;

    gap: 12px;

    margin-bottom: 12px;
}

input[type="text"] {

    width: 100%;

    padding: 12px;

    border: 1px solid #d1d5db;

    border-radius: 8px;

    font-size: 15px;

    outline: none;
}

input[type="text"]:focus {

    border-color: #2563eb;
}


/* =========================================================
   BUTTONS
========================================================= */

button {

    border: none;

    border-radius: 8px;

    padding: 12px 18px;

    cursor: pointer;

    font-weight: bold;

    transition: 0.2s;
}

button:hover {
    transform: translateY(-1px);
}

.add-btn {

    background: #10b981;

    color: white;
}

.remove-btn {

    background: #ef4444;

    color: white;
}

.solve-btn {

    background: #2563eb;

    color: white;

    width: 100%;

    font-size: 17px;

    margin-top: 25px;
}


/* =========================================================
   TRAITS
========================================================= */

.trait-box {

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(190px, 1fr));

    gap: 12px;

    margin-top: 15px;
}

.trait {

    background: #f1f5f9;

    padding: 13px;

    border-radius: 8px;

    cursor: pointer;
}

.trait:hover {

    background: #e2e8f0;
}


/* =========================================================
   STATISTICS
========================================================= */

.stats {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 15px;
}

.stat {

    background: #f8fafc;

    padding: 20px;

    text-align: center;

    border-radius: 12px;
}

.stat-number {

    font-size: 32px;

    font-weight: bold;

    color: #2563eb;

    margin-bottom: 5px;
}


/* =========================================================
   RESULTS
========================================================= */

.result {

    padding: 16px;

    margin: 10px 0;

    border-radius: 10px;
}

.valid {

    background: #dcfce7;

    border-left: 5px solid #16a34a;
}

.invalid {

    background: #fee2e2;

    border-left: 5px solid #dc2626;
}


/* =========================================================
   SEARCH PROCESS
========================================================= */

.process {

    background: #f8fafc;

    padding: 14px;

    margin: 8px 0;

    border-radius: 8px;

    border-left: 4px solid #64748b;
}

.success {

    color: #15803d;

    font-weight: bold;
}

.error {

    color: #b91c1c;

    font-weight: bold;
}


/* =========================================================
   WORKFLOW
========================================================= */

.workflow {

    text-align: center;

    line-height: 2.4;

    font-size: 17px;

    background: #f8fafc;

    padding: 20px;

    border-radius: 10px;
}


/* =========================================================
   INFORMATION
========================================================= */

.info {

    background: #eff6ff;

    border-left: 5px solid #2563eb;

    padding: 15px;

    border-radius: 8px;

    margin-bottom: 20px;
}


/* =========================================================
   FOOTER
========================================================= */

.footer {

    text-align: center;

    color: #64748b;

    padding: 30px;
}


/* =========================================================
   MOBILE
========================================================= */

@media(max-width: 700px) {

    .candidate {

        grid-template-columns: 1fr;
    }

    .stats {

        grid-template-columns: 1fr;
    }

    .header h1 {

        font-size: 28px;
    }

}

</style>

</head>


<body>


<!-- =======================================================
     HEADER
======================================================== -->

<div class="header">

    <h1>
        🧬 Genetic Trait Combination Solver
    </h1>

    <p>
        Backtracking & Constraint Satisfaction
    </p>

    <p>
        Selecting compatible breeding pairings
        under trait rules
    </p>

</div>


<div class="container">


<!-- =======================================================
     INFORMATION
======================================================== -->

<div class="card">

    <div class="info">

        <strong>Real-Time Application:</strong>

        Constraint satisfaction for selecting
        compatible breeding pairings under
        defined trait rules.

    </div>

    <p>

        This application searches possible breeding
        combinations and uses constraints to identify
        combinations that satisfy all required traits.

    </p>

</div>


<!-- =======================================================
     BREEDING CANDIDATES
======================================================== -->

<div class="card">

    <h2>
        🌱 Breeding Candidates
    </h2>

    <p>

        Enter the candidate name and its traits.
        Separate multiple traits using commas.

    </p>


    <form method="POST">


        <input
            type="hidden"
            name="action"
            value="solve"
        >


        <div id="candidates">


            {% for candidate in candidates %}

            <div class="candidate">


                <input
                    type="text"
                    name="candidate_name"
                    value="{{ candidate.name }}"
                    placeholder="Parent name"
                >


                <input
                    type="text"
                    name="candidate_traits"
                    value="{{ candidate.traits | join(', ') }}"
                    placeholder="Trait 1, Trait 2, Trait 3"
                >


                <button
                    type="button"
                    class="remove-btn"
                    onclick="removeCandidate(this)"
                >
                    Remove
                </button>


            </div>

            {% endfor %}


        </div>


        <button
            type="button"
            class="add-btn"
            onclick="addCandidate()"
        >
            + Add Candidate
        </button>


        <hr style="margin:30px 0;">


<!-- =======================================================
     CONSTRAINT SELECTION
======================================================== -->

        <h2>
            ⚙️ Required Traits
        </h2>

        <p>

            Select the traits that the final
            breeding combination must satisfy.

        </p>


        <div class="trait-box">


            {% for trait in all_traits %}

            <label class="trait">

                <input
                    type="checkbox"
                    name="required_traits"
                    value="{{ trait }}"

                    {% if trait in required_traits %}
                    checked
                    {% endif %}
                >

                {{ trait }}

            </label>

            {% endfor %}


        </div>


        <button
            type="submit"
            class="solve-btn"
        >

            🔍 Run Backtracking Solver

        </button>


    </form>

</div>


{% if results is not none %}


<!-- =======================================================
     STATISTICS
======================================================== -->

<div class="card">

    <h2>
        📊 Search Statistics
    </h2>


    <div class="stats">


        <div class="stat">

            <div class="stat-number">

                {{ total_combinations }}

            </div>

            Total Combinations

        </div>


        <div class="stat">

            <div class="stat-number">

                {{ valid_count }}

            </div>

            Valid Combinations

        </div>


        <div class="stat">

            <div class="stat-number">

                {{ invalid_count }}

            </div>

            Rejected Combinations

        </div>


    </div>

</div>


<!-- =======================================================
     VALID RESULTS
======================================================== -->

<div class="card">

    <h2>
        ✅ Compatible Breeding Combinations
    </h2>


    {% if results %}


        {% for pair in results %}

        <div class="result valid">

            <strong>
                ✓ Combination {{ loop.index }}
            </strong>

            <br><br>

            <strong>

                {{ pair[0].name }}
                +
                {{ pair[1].name }}

            </strong>

            <br><br>

            <strong>
                Combined Traits:
            </strong>

            {% set combined = [] %}


            {% for parent in pair %}

                {% for trait in parent.traits %}

                    {% if trait not in combined %}

                        {% set _ =
                            combined.append(trait)
                        %}

                    {% endif %}

                {% endfor %}

            {% endfor %}


            {{ combined | join(', ') }}


        </div>

        {% endfor %}


    {% else %}


        <div class="result invalid">

            ❌ No compatible combination
            satisfies all selected constraints.

        </div>


    {% endif %}


</div>


<!-- =======================================================
     BACKTRACKING PROCESS
======================================================== -->

<div class="card">

    <h2>
        ↩️ Backtracking Search Process
    </h2>


    <p>

        The algorithm checks each possible parent
        pair. If the constraints are not satisfied,
        the combination is rejected and the algorithm
        backtracks to try another combination.

    </p>


    {% for step in search_log %}


        {% if step.status == "VALID" %}


        <div class="process">

            <span class="success">

                ✓ {{ step.pair }}

            </span>

            <br><br>

            {{ step.reason }}

        </div>


        {% else %}


        <div class="process">

            <span class="error">

                ✗ {{ step.pair }}

            </span>

            <br><br>

            {{ step.reason }}

            → <strong>BACKTRACK</strong>

        </div>


        {% endif %}


    {% endfor %}


</div>


<!-- =======================================================
     ALGORITHM WORKFLOW
======================================================== -->

<div class="card">

    <h2>
        🔄 Algorithm Workflow
    </h2>


    <div class="workflow">

        Candidate Data

        ↓

        Required Traits

        ↓

        Generate Parent Pair

        ↓

        Check Constraints

        ↓

        Valid → Save Solution

        <br>

        Invalid → Backtrack

        ↓

        Try Next Combination

        ↓

        Display Results

    </div>

</div>


{% endif %}


<!-- =======================================================
     ABOUT
======================================================== -->

<div class="card">

    <h2>
        🧠 About Backtracking & CSP
    </h2>


    <p>

        <strong>Constraint Satisfaction Problem:</strong>

        The breeding problem is represented using
        candidates, traits, and breeding requirements.

    </p>


    <p>

        <strong>Backtracking:</strong>

        The algorithm explores possible parent
        combinations. When a combination violates
        the required constraints, it goes back and
        tries another combination.

    </p>


    <p>

        This reduces unnecessary search and provides
        a systematic method for finding compatible
        breeding combinations.

    </p>

</div>


</div>


<!-- =======================================================
     FOOTER
======================================================== -->

<div class="footer">

    Genetic Trait Combination Solver

    <br>

    Backtracking & Constraint Satisfaction

</div>


<!-- =======================================================
     JAVASCRIPT
======================================================== -->

<script>


function addCandidate() {

    const container =
        document.getElementById(
            "candidates"
        );


    const div =
        document.createElement(
            "div"
        );


    div.className =
        "candidate";


    div.innerHTML = `

        <input
            type="text"
            name="candidate_name"
            placeholder="Parent name"
        >

        <input
            type="text"
            name="candidate_traits"
            placeholder="Trait 1, Trait 2, Trait 3"
        >

        <button
            type="button"
            class="remove-btn"
            onclick="removeCandidate(this)"
        >

            Remove

        </button>

    `;


    container.appendChild(div);

}


function removeCandidate(button) {

    const candidates =
        document.querySelectorAll(
            ".candidate"
        );


    if (candidates.length > 2) {

        button.parentElement.remove();

    }

    else {

        alert(
            "At least two candidates are required."
        );

    }

}


</script>


</body>

</html>
"""


# ============================================================
# GET ALL TRAITS
# ============================================================

def get_all_traits(candidates):

    traits = set()

    for candidate in candidates:

        traits.update(
            candidate["traits"]
        )

    return sorted(traits)


# ============================================================
# CONSTRAINT CHECKER
# ============================================================

def check_constraints(
    pair,
    required_traits
):

    combined_traits = set()

    for parent in pair:

        combined_traits.update(
            parent["traits"]
        )

    missing_traits = [
        trait
        for trait in required_traits
        if trait not in combined_traits
    ]

    if not missing_traits:

        return True, []

    return False, missing_traits


# ============================================================
# BACKTRACKING SOLVER
# ============================================================

def backtracking_solver(
    candidates,
    required_traits
):

    valid_solutions = []

    search_log = []


    def backtrack(
        start,
        selected
    ):

        # ----------------------------------------------------
        # BASE CASE
        # ----------------------------------------------------

        if len(selected) == 2:

            names = [
                parent["name"]
                for parent in selected
            ]

            pair_name = (
                names[0]
                + " + "
                + names[1]
            )


            valid, missing = check_constraints(
                selected,
                required_traits
            )


            if valid:

                valid_solutions.append(
                    selected.copy()
                )


                search_log.append({

                    "pair": pair_name,

                    "status": "VALID",

                    "reason":
                        "All constraints satisfied"

                })


            else:

                search_log.append({

                    "pair": pair_name,

                    "status": "INVALID",

                    "reason":
                        "Missing: "
                        + ", ".join(missing)

                })


            return


        # ----------------------------------------------------
        # TRY NEXT CANDIDATE
        # ----------------------------------------------------

        for i in range(
            start,
            len(candidates)
        ):

            selected.append(
                candidates[i]
            )


            # Recursively explore
            backtrack(
                i + 1,
                selected
            )


            # ------------------------------------------------
            # BACKTRACK
            # ------------------------------------------------

            selected.pop()


    backtrack(
        0,
        []
    )


    return (
        valid_solutions,
        search_log
    )


# ============================================================
# MAIN ROUTE
# ============================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)

def index():

    candidates = [
        {
            "name": candidate["name"],
            "traits": candidate["traits"].copy()
        }

        for candidate in DEFAULT_CANDIDATES
    ]


    results = None

    search_log = []

    required_traits = []

    total_combinations = 0

    valid_count = 0

    invalid_count = 0


    # ========================================================
    # FORM SUBMISSION
    # ========================================================

    if request.method == "POST":


        names = request.form.getlist(
            "candidate_name"
        )


        traits_list = request.form.getlist(
            "candidate_traits"
        )


        required_traits = request.form.getlist(
            "required_traits"
        )


        # ----------------------------------------------------
        # BUILD CANDIDATE LIST
        # ----------------------------------------------------

        candidates = []


        for name, traits_string in zip(
            names,
            traits_list
        ):

            name = name.strip()


            if name:

                traits = [

                    trait.strip()

                    for trait
                    in traits_string.split(",")

                    if trait.strip()

                ]


                candidates.append({

                    "name": name,

                    "traits": traits

                })


        # ----------------------------------------------------
        # RUN BACKTRACKING
        # ----------------------------------------------------

        if len(candidates) >= 2:

            (
                results,
                search_log
            ) = backtracking_solver(

                candidates,

                required_traits

            )


            total_combinations = len(

                list(

                    combinations(

                        candidates,

                        2

                    )

                )

            )


            valid_count = len(results)


            invalid_count = (

                total_combinations
                - valid_count

            )


    # ========================================================
    # TRAITS
    # ========================================================

    all_traits = get_all_traits(
        candidates
    )


    # ========================================================
    # RENDER PAGE
    # ========================================================

    return render_template_string(

        HTML,

        candidates=candidates,

        all_traits=all_traits,

        required_traits=required_traits,

        results=results,

        search_log=search_log,

        total_combinations=
            total_combinations,

        valid_count=
            valid_count,

        invalid_count=
            invalid_count

    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
