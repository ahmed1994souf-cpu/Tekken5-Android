extends Node3D

var player: CharacterBody3D
var enemy: CharacterBody3D
var player_speed := 4.5
var enemy_speed := 2.4
var attack_cooldown := 0.0

func _ready() -> void:
    _build_arena()
    player = _make_fighter(Vector3(-2.5, 1.0, 0.0), true)
    enemy = _make_fighter(Vector3(2.5, 1.0, 0.0), false)
    _make_camera()

func _physics_process(delta: float) -> void:
    if player == null or enemy == null:
        return
    _player_update(delta)
    _enemy_update(delta)
    attack_cooldown = maxf(attack_cooldown - delta, 0.0)

func _player_update(delta: float) -> void:
    var input_vec := Vector2.ZERO
    if Input.is_key_pressed(KEY_A): input_vec.x -= 1.0
    if Input.is_key_pressed(KEY_D): input_vec.x += 1.0
    if Input.is_key_pressed(KEY_W): input_vec.y -= 1.0
    if Input.is_key_pressed(KEY_S): input_vec.y += 1.0
    var dir := Vector3(input_vec.x, 0.0, input_vec.y).normalized()
    player.velocity.x = dir.x * player_speed
    player.velocity.z = dir.z * player_speed
    player.velocity.y = -0.5
    player.move_and_slide()
    player.look_at(Vector3(enemy.global_position.x, player.global_position.y, enemy.global_position.z), Vector3.UP)
    if Input.is_key_pressed(KEY_J) and attack_cooldown <= 0.0:
        _attack(player, enemy)
        attack_cooldown = 0.45
    if Input.is_key_pressed(KEY_K) and attack_cooldown <= 0.0:
        _grapple(player, enemy)
        attack_cooldown = 0.7

func _enemy_update(delta: float) -> void:
    var to_player := player.global_position - enemy.global_position
    to_player.y = 0.0
    var distance := to_player.length()
    if distance > 1.8:
        var dir := to_player.normalized()
        enemy.velocity.x = dir.x * enemy_speed
        enemy.velocity.z = dir.z * enemy_speed
        enemy.velocity.y = -0.5
        enemy.move_and_slide()
    else:
        enemy.velocity = Vector3.ZERO
        enemy.look_at(Vector3(player.global_position.x, enemy.global_position.y, player.global_position.z), Vector3.UP)
        if attack_cooldown <= 0.0:
            _attack(enemy, player)
            attack_cooldown = 0.8

func _attack(attacker: Node3D, target: Node3D) -> void:
    if attacker.global_position.distance_to(target.global_position) <= 2.0:
        target.position.y += 0.08

func _grapple(attacker: Node3D, target: Node3D) -> void:
    if attacker.global_position.distance_to(target.global_position) <= 2.0:
        target.global_position = attacker.global_position + -attacker.global_transform.basis.z * 0.9

func _build_arena() -> void:
    var floor := StaticBody3D.new()
    var mesh := MeshInstance3D.new()
    var box := BoxMesh.new()
    box.size = Vector3(14.0, 0.25, 10.0)
    mesh.mesh = box
    floor.add_child(mesh)
    var shape := CollisionShape3D.new()
    var collider := BoxShape3D.new()
    collider.size = box.size
    shape.shape = collider
    floor.add_child(shape)
    floor.position.y = -0.15
    add_child(floor)

func _make_fighter(pos: Vector3, is_player: bool) -> CharacterBody3D:
    var body := CharacterBody3D.new()
    body.position = pos
    var mesh := MeshInstance3D.new()
    var capsule := CapsuleMesh.new()
    capsule.height = 1.8
    capsule.radius = 0.42
    mesh.mesh = capsule
    body.add_child(mesh)
    var shape := CollisionShape3D.new()
    var collider := CapsuleShape3D.new()
    collider.height = 1.8
    collider.radius = 0.42
    shape.shape = collider
    body.add_child(shape)
    add_child(body)
    return body

func _make_camera() -> void:
    var camera := Camera3D.new()
    camera.position = Vector3(0.0, 7.0, 10.0)
    camera.look_at(Vector3.ZERO, Vector3.UP)
    add_child(camera)
