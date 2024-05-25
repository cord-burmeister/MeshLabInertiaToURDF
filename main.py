import pymeshlab
import argparse


def calculate_inertial_tag(file_name=None, mass=-1, pr=8, scale_factor=100, urdf_output=True):
    ms = pymeshlab.MeshSet()

    if file_name is None:
        print('Please put the input file to the same folder as this script and type in the full name of your file.')
        file_name = input()
    ms.load_new_mesh(file_name)

    if mass < 0:
        print('Please type the mass of your object in kg')
        mass = float(input())

    print('Calculating the center of mass')
    geom = ms.get_geometric_measures()
    com = geom['barycenter']

    print('Scaling the mesh')
    ms.compute_matrix_from_scaling_or_normalization(axisx=scale_factor, axisy=scale_factor, axisz=scale_factor)

    print('Generating the convex hull of the mesh')
    ms.generate_convex_hull()  # TODO only if object is not watertight

    print('Calculating intertia tensor')
    geom = ms.get_geometric_measures()
    volume = geom['mesh_volume']
    tensor = geom['inertia_tensor'] / pow(scale_factor, 2) * mass / volume

    if urdf_output:
        intertial_xml = f'<inertial>\n  <origin xyz="{com[0]:.{pr}f} {com[1]:.{pr}f} {com[2]:.{pr}f}"/>\n  <mass value="{mass:.{pr}f}"/>\n  <inertia ixx="{tensor[0, 0]:.{pr}f}" ixy="{tensor[1, 0]:.{pr}f}" ixz="{tensor[2, 0]:.{pr}f}" iyy="{tensor[1, 1]:.{pr}f}" iyz="{tensor[1, 2]:.{pr}f}" izz="{tensor[2, 2]:.{pr}f}"/>\n</inertial>'
        print(intertial_xml)

    if not urdf_output:
        intertial_xml = f'<inertial>\n  <pose> {com[0]:.{pr}f} {com[1]:.{pr}f} {com[2]:.{pr}f} 0 0 0 </pose>\n  <mass>{mass:.{pr}f}</mass>\n  <inertia>\n  <inertia>\n   <ixx>{tensor[0, 0]:.{pr}f}</ixx> \n   <ixy>{tensor[1, 0]:.{pr}f}</ixy>\n   <ixz>{tensor[2, 0]:.{pr}f}</ixz>\n   <iyy>{tensor[1, 1]:.{pr}f}</iyy>\n   <iyz>{tensor[1, 2]:.{pr}f}</iyz>\n   <izz>{tensor[2, 2]:.{pr}f} </izz>\n  </inertia>\n</inertial>'
        print(intertial_xml)


if __name__ == '__main__':

    file_name=None 
    mass=-1 
    pr=8 
    scale_factor=100
    urdf_output=True

    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', dest='file_name', type=str, help='Add filename of the DAE or STL file to calculate the inertial from')
    parser.add_argument('--mass', dest='mass', type=float, nargs='?', const=1.0, help='Add the mass of the object')
    parser.add_argument('--scale_factor', dest='scale_factor', nargs='?', const=100.0, type=float, help='Define the internal scale factor to improve precision')
    parser.add_argument('--float_precision', dest='float_precision', nargs='?', const=8, type=float, help='Define the precision of the float in the output')
    parser.add_argument('--urdf_output', dest='urdf_output', type=str, choices=['True', 'False'], nargs='?', const="True", help='flag indicating if output is urdf or sdf format')
    args = parser.parse_args()

    print (args)

    if args.mass is not None:
        mass = args.mass
    if args.scale_factor is not None:
        scale_factor = args.scale_factor
    if args.float_precision is not None:
        pr = args.float_precision
    if args.urdf_output is not None:
        urdf_output = args.urdf_output == "True"

    calculate_inertial_tag(file_name = args.file_name, mass=mass, scale_factor=scale_factor, pr =pr, urdf_output = urdf_output )  
