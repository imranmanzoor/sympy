from sympy import symbols, Matrix, sin, cos
from sympy.physics.classical.essential import Vector, ReferenceFrame
from sympy.physics.classical.functions import dot, cross, dynamicsymbols

phi, x, y, z = symbols('phi x y z')
A = ReferenceFrame('A')

def test_ang_vel():
    ((q0, q1, q2, q3, q4), (q0d, q1d, q2d, q3d, q4d)) = dynamicsymbols('q', 5, 1)
    N = ReferenceFrame('N')
    A = N.orientnew('A', 'Simple', q1, 3)
    B = A.orientnew('B', 'Simple', q2, 1)
    C = B.orientnew('C', 'Simple', q3, 2)
    D = N.orientnew('D', 'Simple', q4, 2)
    u0, u1, u2 = dynamicsymbols('u', 3)
    assert A.ang_vel_in(N) == (q1d)*A.z
    assert B.ang_vel_in(N) == (q2d)*B.x + (q1d)*A.z
    assert C.ang_vel_in(N) == (q3d)*C.y + (q2d)*B.x + (q1d)*A.z

    A2 = N.orientnew('A2', 'Simple', q4, 2)
    assert N.ang_vel_in(N) == 0
    assert N.ang_vel_in(A) == -q1d*N.z
    assert N.ang_vel_in(B) == -q1d*A.z - q2d*B.x
    assert N.ang_vel_in(C) == -q1d*A.z - q2d*B.x - q3d*B.y
    assert N.ang_vel_in(A2) == -q4d*N.y

    assert A.ang_vel_in(N) == q1d*N.z
    assert A.ang_vel_in(A) == 0
    assert A.ang_vel_in(B) == - q2d*B.x
    assert A.ang_vel_in(C) == - q2d*B.x - q3d*B.y
    assert A.ang_vel_in(A2) == q1d*N.z - q4d*N.y

    assert B.ang_vel_in(N) == q1d*A.z + q2d*A.x
    assert B.ang_vel_in(A) == q2d*A.x
    assert B.ang_vel_in(B) == 0
    assert B.ang_vel_in(C) == -q3d*B.y
    assert B.ang_vel_in(A2) == q1d*A.z + q2d*A.x - q4d*N.y

    assert C.ang_vel_in(N) == q1d*A.z + q2d*A.x + q3d*B.y
    assert C.ang_vel_in(A) == q2d*A.x + q3d*C.y
    assert C.ang_vel_in(B) == q3d*B.y
    assert C.ang_vel_in(C) == 0
    assert C.ang_vel_in(A2) == q1d*A.z + q2d*A.x + q3d*B.y - q4d*N.y

    assert A2.ang_vel_in(N) == q4d*A2.y
    assert A2.ang_vel_in(A) == q4d*A2.y - q1d*N.z
    assert A2.ang_vel_in(B) == q4d*N.y - q1d*A.z - q2d*A.x
    assert A2.ang_vel_in(C) == q4d*N.y - q1d*A.z - q2d*A.x - q3d*B.y
    assert A2.ang_vel_in(A2) == 0

    C.set_ang_vel(N, u0*C.x + u1*C.y + u2*C.z)
    assert C.ang_vel_in(N) == (u0)*C.x + (u1)*C.y + (u2)*C.z
    assert N.ang_vel_in(C) == (-u0)*C.x + (-u1)*C.y + (-u2)*C.z
    assert C.ang_vel_in(D) == (u0)*C.x + (u1)*C.y + (u2)*C.z + (-q4d)*D.y
    assert D.ang_vel_in(C) == (-u0)*C.x + (-u1)*C.y + (-u2)*C.z + (q4d)*D.y


def test_dcm():
    q0, q1, q2, q3, q4 = dynamicsymbols('q', 5)
    N = ReferenceFrame('N')
    A = N.orientnew('A', 'Simple', q1, 3)
    B = A.orientnew('B', 'Simple', q2, 1)
    C = B.orientnew('C', 'Simple', q3, 2)
    D = N.orientnew('D', 'Simple', q4, 2)
    assert N.dcm(C) == Matrix([
        [- sin(q1) * sin(q2) * sin(q3) + cos(q1) * cos(q3), - sin(q1) *
        cos(q2), sin(q1) * sin(q2) * cos(q3) + sin(q3) * cos(q1)], [sin(q1) *
        cos(q3) + sin(q2) * sin(q3) * cos(q1), cos(q1) * cos(q2), sin(q1) *
        sin(q3) - sin(q2) * cos(q1) * cos(q3)], [- sin(q3) * cos(q2), sin(q2),
        cos(q2) * cos(q3)]])
    # This is a little touchy.  Is it ok to use simplify in assert?
    assert D.dcm(C) == Matrix(
        [[cos(q1) * cos(q3) * cos(q4) - sin(q3) * (- sin(q4) * cos(q2) +
        sin(q1) * sin(q2) * cos(q4)), - sin(q2) * sin(q4) - sin(q1) *
        cos(q2) * cos(q4), sin(q3) * cos(q1) * cos(q4) + cos(q3) * (- sin(q4) *
        cos(q2) + sin(q1) * sin(q2) * cos(q4))], [sin(q1) * cos(q3) +
        sin(q2) * sin(q3) * cos(q1), cos(q1) * cos(q2), sin(q1) * sin(q3) -
        sin(q2) * cos(q1) * cos(q3)], [sin(q4) * cos(q1) * cos(q3) -
        sin(q3) * (cos(q2) * cos(q4) + sin(q1) * sin(q2) * sin(q4)), sin(q2) *
        cos(q4) - sin(q1) * sin(q4) * cos(q2), sin(q3) * sin(q4) * cos(q1) +
        cos(q3) * (cos(q2) * cos(q4) + sin(q1) * sin(q2) * sin(q4))]])

def test_Vector():
    v1 = x*A.x + y*A.y + z*A.z
    v2 = x**2*A.x + y**2*A.y + z**2*A.z
    v3 = v1 + v2
    v4 = v1 - v2

    assert isinstance(v1, Vector)
    assert dot(v1, A.x) == x
    assert dot(v1, A.y) == y
    assert dot(v1, A.z) == z

    assert isinstance(v2, Vector)
    assert dot(v2, A.x) == x**2
    assert dot(v2, A.y) == y**2
    assert dot(v2, A.z) == z**2

    assert isinstance(v3, Vector)
    # We probably shouldn't be using simplify in dot...
    assert dot(v3, A.x) == x + x**2
    assert dot(v3, A.y) == y + y**2
    assert dot(v3, A.z) == z + z**2

    assert isinstance(v4, Vector)
    # We probably shouldn't be using simplify in dot...
    assert dot(v4, A.x) == x - x**2
    assert dot(v4, A.y) == y - y**2
    assert dot(v4, A.z) == z - z**2



    #TODO: Put some tests here, mew.
