from flask import Flask, request, jsonify, abort

from safetynet.profiles import (
    create_profile,
    update_profile,
    get_profile,
    get_profiles,
    get_nearby_profiles,
)

app = Flask(__name__)


@app.route("/api/profiles", methods=["GET", "POST"])
def profiles():
    if request.method == "POST":
        profile = create_profile(request.json)
        return jsonify({"profile": profile.to_dict(), "token": profile.token()})
    elif request.method == "GET":
        # extract long and lat from the url and send to get nearby profiles
        lat = request.args.get("latitude", None)
        lon = request.args.get("longitude", None)
        if lat is None or lon is None:
            return jsonify([p.to_dict() for p in get_profiles()])
        return jsonify(
            [p.to_dict() for p in get_nearby_profiles(float(lat), float(lon))]
        )


@app.route("/api/profiles/<int:profile_id>", methods=["POST"])
def api_update_profile(profile_id):
    j = request.json
    unsafe_token = j["token"]
    profile = get_profile(profile_id)
    if unsafe_token != profile.token():
        abort(401)
    profile = update_profile(j["profile"], profile_id)
    return jsonify(profile.to_dict())


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/profile")
def profile():
    return app.send_static_file("profile.html")


@app.route("/map")
def route_map():
    return app.send_static_file("googlemap.html")


if __name__ == "__main__":
    app.run(debug=True)
