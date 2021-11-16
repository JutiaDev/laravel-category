<?php

namespace JutiaDev\Category\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use JutiaDev\Category\Contracts\Category as CategoryContract;
use Swagger\Annotations as SWG;

/**
 * JutiaDev\Category\Models\Category
 *
 * @SWG\Definition (
 *      definition="Category",
 *      required={
 *          "name",
 *          "left",
 *          "righ",
 *          "depth",
 *      },
 *      @SWG\Property(
 *          property="id",
 *          description="id",
 *          type="integer",
 *          format="int32"
 *      ),
 *      @SWG\Property(
 *          property="name",
 *          description="Category Name",
 *          type="string"
 *      ),
 *      @SWG\Property(
 *          property="description",
 *          description="Category Description",
 *          type="string"
 *      ),
 *      @SWG\Property(
 *          property="picture",
 *          description="Category Picture",
 *          type="string"
 *      ),
 *      @SWG\Property(
 *          property="enabled",
 *          description="Indicate wether the category is enabled",
 *          type="boolean"
 *      ),
 *      @SWG\Property(
 *          property="left",
 *          description="left",
 *          type="integer",
 *          format="int32"
 *      ),
 *      @SWG\Property(
 *          property="righ",
 *          description="righ",
 *          type="integer",
 *          format="int32"
 *      ),
 *      @SWG\Property(
 *          property="depth",
 *          description="depth",
 *          type="integer",
 *          format="int32"
 *      )
 * )
 * @method static \Illuminate\Database\Eloquent\Builder|Category newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|Category newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|Category query()
 * @mixin \Eloquent
 */
class Category extends Model implements CategoryContract
{
    use HasFactory;

    public const CATEGORY = 'category';
    public const CATEGORIES = 'categories';

    public const ID = 'id';
    public const PID = 'pid';
    public const NAME = 'name';
    public const DESCRIPTION = 'description';
    public const PICTURE = 'picture';
    public const ENABLED = 'enabled';
    public const LEFT = 'left';
    public const RIGHT = 'right';
    public const DEPTH = 'depth';

    /**
     * Validation rules
     *
     * @var array
     */
    public static $default_rules = [];

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    public $fillable = [];

    /**
     * Get the table associated with the model.
     *
     * @return string
     */
    public function getTable()
    {
        return 'categories';
    }

}
