
<'
package vr_ad;
import vr_ad/e/vr_ad_top;

//A struct representing a register and the access amount by type
struct reg_use {
    %name : string;
    %read_count : int;
    %write_count : int;
};

//A static variable containing all of the reg_use structs
struct reg_usage {
	static reg_uses : list (key: name) of reg_use = {};
};

extend sys {
    post_generate() is also {
        set_config(print, radix, hex);
    };
    
    @import_python(module_name="create_heatmap", python_name="draw_heatmap")
    draw_heatmap(all_reg_info : list of reg_use) is imported;

    //Increments the write access amount of the given register
    add_write(reg_str : string) is {
	    var existing_reg_use : reg_use = reg_usage::reg_uses.key(reg_str);
	    if existing_reg_use == NULL then {
		    var new_reg : reg_use = new with {
			        					.name = reg_str;
			        					.write_count = 1;
		        					};
		    reg_usage::reg_uses.push(new_reg);
	    }
	    else {
		    existing_reg_use.write_count += 1;
	    };
    };
    
    //Increments the read access amount of the given register
    add_read(reg_str : string) is {
	    var existing_reg_use : reg_use = reg_usage::reg_uses.key(reg_str);
	    if existing_reg_use == NULL then {
		    var new_reg : reg_use = new with {
			        					.name = reg_str;
			        					.read_count = 1;
		        					};
		    reg_usage::reg_uses.push(new_reg);
	    }
	    else {
		    existing_reg_use.read_count += 1;
	    };
    };
    
    //Runs at the end of the tests and draws the heatmap
    extract() is also {
	    draw_heatmap(reg_usage::reg_uses.as_a(list of reg_use));
    };
};


extend vr_ad_sequence_driver {
    send_to_bfm(ad_item:  vr_ad_operation) @clock is also {
        if ad_item is a REG vr_ad_operation (reg_op) {
            out( ">>>>>>>>>>>>>>>>>>>>>>>> ", ad_item.direction, " ", reg_op.reg.kind, " ", ad_item.address );
            if ad_item.direction.as_a(string) == "READ" then {
            	sys.add_read(reg_op.reg.kind.as_a(string));
            };
            if ad_item.direction.as_a(string) == "WRITE" then {
            	sys.add_write(reg_op.reg.kind.as_a(string));
            };
        } else {
            out( ">>>>>>>>>>>>>>>>>>>>>>>> ", ad_item.direction, " ", ad_item.address  );
        } 
    };
};



'>

Run examples:

specman -64 -c 'load vr_ad/examples/vr_ad_reg_cover.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_rw_from_any_tcm.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_mult_module_evc.e map_report; test' 
specman -64 -c 'load vr_ad/examples/vr_ad_tf_rw_from_any_tcm.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_reg_file_random_access.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_access_a_reference.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_rw_from_any_tcm.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_tf_mult_maps_on_bus.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_mult_bfms.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_tf_mult_regs.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_tf_side_effects.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_tf_indirect_access.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_tf_access_a_reference.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_tf_mult_bfms.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_update_while_reading.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_broadcast.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_tf_twin_regs.e map_report; test'
specman -64 -c 'load vr_ad/examples/vr_ad_module_evc_regs.e map_report; test'

  